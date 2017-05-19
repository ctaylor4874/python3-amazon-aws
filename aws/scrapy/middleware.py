import os
import logging
import time

from aws.parsers import ItemSearchResponse
from aws.parsers.base import ItemSearchErrorResponse
from aws.parsers.errors import ItemSearchError, RequestThrottledError, RequestExpiredError

class ApiResponseDownloaderMiddleware(object):
    root = os.path.dirname(os.path.abspath(__file__))
    write_response_fp = os.path.join(root, 'response.xml')
    error_response_fp = os.path.join(root, 'error-response.xml')

    def __init__(self, crawler):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.crawler = crawler
        self.settings = self.crawler.settings
        self.stats = self.crawler.stats
        self.max_retry_times = self.settings.getint('AWS_REQUEST_THROTTLED_RETRY_TIMES')
        self.priority_adjust = self.settings.getint('AWS_REQUEST_THROTTLED_RETRY_PRIORITY_ADJUST')
        self.write_responses = self.settings.getbool('WRITE_RESPONSES')

    def _raise_for_request_error(self, parser):
        """
        If the request was not valid, raise the errors associated with it.
        :return: 
        """
        if not parser.items.request.is_valid:
            if parser.items.request.errors:
                raise ItemSearchError.from_element(parser.items.request.errors[0])
            raise ItemSearchError('UNKNOWN_ERROR', 'Request failed but no error was found')

    def _retry(self, request, reason, spider):
        retries = request.meta.get('retry_times', 0) + 1
        timeout = request.meta.get('timeout', 1) ** 2

        if retries <= self.max_retry_times:
            time.sleep(timeout)
            self.logger.debug("Retrying %(request)s (failed %(retries)d times): %(reason)s - Timeout set to %(timeout)s",
                              {'request': request, 'retries': retries, 'reason': reason, 'timeout': timeout},
                              extra={'spider': spider})
            retryreq = request.copy()
            retryreq.meta['retry_times'] = retries
            retryreq.meta['timeout'] = 2 if timeout == 1 else timeout
            retryreq.dont_filter = True
            retryreq.priority = request.priority + self.priority_adjust
            return retryreq
        else:
            self.logger.debug("Gave up retrying %(request)s (failed %(retries)d times): %(reason)s",
                              {'request': request, 'retries': retries, 'reason': reason},
                              extra={'spider': spider})

    def process_response(self, request, response, spider):
        if self.write_responses:
            with open(self.write_response_fp, 'wb') as f:
                f.write(response.body)

        # Raise for any potential error which could have been brought back.
        # This is needed because instead of wrapping the error in the response,
        # they just send back the error as a body.xml
        # Ex the body will just be <ItemSearchError><!-- error stuff here --></ItemSearchError>
        potential_err = ItemSearchErrorResponse.from_string(response.body)
        try:
            potential_err.raise_for_error()
        except RequestThrottledError as e:
            self.stats.inc_value('request_throttled')
            self.logger.debug(e)
            return self._retry(request, 'RequestThrottled', spider) or response
        except RequestExpiredError as e:
            # Request will expire sometimes because the request object will sit in the queue to long and
            # the signature will no longer match when the engine finally sends the request out.
            self.stats.inc_value('request_expired')
            self.logger.debug(e)
            return self._retry(request, 'RequestExpired', spider) or response
        except:
            with open(self.error_response_fp, 'wb') as f:
                f.write(response.body)
            raise

        # Now parse the body and raise for any request errors.
        # This is different from above because the response is actually what we expect, its just that
        # if the request failed due to parameters, there will be an error contained in the <Request> part of the
        # xml.
        parser = ItemSearchResponse.from_string(response.body)
        self._raise_for_request_error(parser)
        return response

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)
