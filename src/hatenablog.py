import logging

import requests
from requests.auth import HTTPBasicAuth
from xml.sax.saxutils import escape

logger = logging.getLogger()


def post_hatenablog(secret_hatenablog: dict, blog_title: str, blog_body: str, is_draft: str = "no", category: str = "読書メーター"):
    logger.info("post hatenablog")

    url = f"https://blog.hatena.ne.jp/{secret_hatenablog['hatena_id']}/{secret_hatenablog['blog_domain']}/atom/entry"
    headers = {'Content-Type': 'application/xml'}
    data = f"""
<?xml version="1.0" encoding="utf-8"?>
<entry xmlns="http://www.w3.org/2005/Atom" xmlns:app="http://www.w3.org/2007/app">
    <title>{blog_title}</title>
    <author><name>{secret_hatenablog['hatena_id']}</name></author>
    <content type="text/x-markdown">{escape(blog_body)}<br/><br/>posted by AWS Lambda</content>
    <category term="{category}"/>
    <app:control>
        <app:draft>{is_draft}</app:draft>
    </app:control>
</entry>
    """
    auth = HTTPBasicAuth(
        secret_hatenablog["hatena_id"],
        secret_hatenablog["api_key"])

    logger.debug(f"data={data}")

    response = requests.post(
        url=url,
        headers=headers,
        data=data.replace('\n', '').encode("utf-8"),
        auth=auth)

    logger.info(f"response.content={response.content}")
    logger.debug(f"response.text={response.text}")

    return response
