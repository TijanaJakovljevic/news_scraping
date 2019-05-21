from scrapy.downloadermiddlewares.retry import RetryMiddleware
from scrapy.utils.response import response_status_message


class CustomRetryMiddleware(RetryMiddleware):
    def process_response(self, request, response, spider):
        if request.meta.get("dont_retry", False):
            return response

        # Kurir 408 save
        if response.status == 408 and spider.spider_path:
            self._save_failed_url(response.url, spider.spider_path)
            return response

        if response.status in self.retry_http_codes:
            reason = response_status_message(response.status)
            return self._retry(request, reason, spider) or response

        return response

    @staticmethod
    def _save_failed_url(url, spider_path):
        with open(f"{spider_path}/failed_urls.txt", "a") as urls_fle:
            urls_fle.write("{}\n".format(url))
