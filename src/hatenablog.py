import logging

import requests
from requests.auth import HTTPBasicAuth

logger = logging.getLogger()


def post_hatenablog(secret_hatenablog: dict, blog_title: str, blog_body: str, is_draft: str = "no", category: str = "読書メーター"):
    logger.info("post hatenablog")

    url_text = f"https://blog.hatena.ne.jp/{secret_hatenablog['hatena_id']}/{secret_hatenablog['blog_domain']}/atom/entry"

    headers = {'Content-Type': 'application/xml'}

    data = f"""
<?xml version="1.0" encoding="utf-8"?>
<entry xmlns="http://www.w3.org/2005/Atom" xmlns:app="http://www.w3.org/2007/app">
    <title>{blog_title}</title>
    <author><name>{secret_hatenablog['hatena_id']}</name></author>
    <content type="text/plain">
        {blog_body}
    </content>
    <category term="{category}" />
    <app:control>
        <app:draft>{is_draft}</app:draft>
    </app:control>
</entry>
    """
    logger.debug(f"data={data}")

    response = requests.post(
        url=url_text,
        headers=headers,
        data=data.replace('\n', '').encode("utf-8"),
        auth=HTTPBasicAuth(
            secret_hatenablog["hatena_id"],
            secret_hatenablog["api_key"]))

    logger.info(response.content)

    return response
