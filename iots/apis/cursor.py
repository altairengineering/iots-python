from dataclasses import dataclass
from typing import Union, overload

from ..internal.resource import APIResource
from ..models import models, primitives


@dataclass
class Cursor1(APIResource):
    cursor_id: str

    def post(self, req: Union[models.ThenQueryRequest, dict], **kwargs) -> Union[models.PostAPICursorResponse, primitives.NoResponse]:
        """
        If the cursor is still alive, returns an object with the following
        attributes:

        - *id*: the *cursor-identifier*
        - *result*: a list of documents for the current batch
        - *hasMore*: *false* if this was the last batch
        - *count*: if present the total number of elements

        Note that even if *hasMore* returns *true*, the next call might
        still return no documents. If, however, *hasMore* is *false*, then
        the cursor is exhausted.  Once the *hasMore* attribute has a value of
        *false*, the client can stop.

        > 📘 **Information:** This endpoint is compatible with the
        > [`/_api/cursor/{cursor-identifier}`](https://www.arangodb.com/docs/stable/http/aql-query-cursor-accessing-cursors.html#read-next-batch-from-cursor)
        > in the ArangoDB REST API.

        :param req: Request payload.
        :type req: Union[models.ThenQueryRequest, dict]
        :return: The API response to the request.
        :rtype: Union[models.PostAPICursorResponse, primitives.NoResponse]
        """
        req_content_types = [
            ("application/json", models.ThenQueryRequest),
        ]

        resp = self._make_request("POST", req, req_content_types=req_content_types, **kwargs)
        return self._handle_response(resp, [
            (200, "application/json", models.PostAPICursorResponse),
            (400, "", primitives.NoResponse),
            (401, "application/json", models.ErrorResponse),
            (403, "application/json", models.ErrorResponse),
            (404, "", primitives.NoResponse),
            (405, "", primitives.NoResponse),
            (500, "application/json", models.ErrorResponse),
        ])

    def _build_partial_path(self):
        return f"/cursor/{self.cursor_id}"


@dataclass
class Cursor2(APIResource):

    def post(self, req: Union[models.PostAPICursor, dict], **kwargs) -> Union[models.PostAPICursorResponse, models.ErrorResponse, primitives.NoResponse]:
        """
        This endpoint allows to perform custom read-only queries directly on AnythingDB.
        AnythingDB relies on [**ArangoDB**](https://www.arangodb.com/), so this endpoint
        allows to set a custom AQL query that will run in a sandboxed ArangoDB database
        where the AnythingDB's Space information is stored.

        > 📘 **Information:** This endpoint is compatible with the
        > [`/_api/cursor`](https://www.arangodb.com/docs/stable/http/aql-query-cursor-accessing-cursors.html#create-cursor)
        > in the ArangoDB REST API.

        **A JSON object with these properties is required:**

          - **query**: contains the query string to be executed. **Note: Only read-only queries are allowed.**
          - **count**: indicates whether the number of documents in the result set should be returned in
           the "count" attribute of the result.
           Calculating the "count" attribute might have a performance impact for some queries
           in the future so this option is turned off by default, and "count"
           is only returned when requested.
          - **batchSize**: maximum number of result documents to be transferred from
           the server to the client in one roundtrip. If this attribute is
           not set, a server-controlled default value will be used. A *batchSize* value of
           *0* is disallowed. **Note: the server will set a maximum value.**
          - **ttl**: The time-to-live for the cursor (in seconds). If the result set is small enough
           (less than or equal to `batchSize`) then results are returned right away.
           Otherwise they are stored in memory and will be accessible via the cursor with
           respect to the `ttl`. The cursor will be removed on the server automatically
           after the specified amount of time. This is useful to ensure garbage collection
           of cursors that are not fully fetched by clients. If not set, a server-defined
           value will be used (default: 30 seconds). **Note: the server will set a maximum value.**
          - **cache**: flag to determine whether the AQL query results cache
           shall be used. **Note: This value is fixed to *false*.**
          - **memoryLimit**: the maximum number of memory (measured in bytes) that the query is allowed to
           use. If set, then the query will fail with error "resource limit exceeded" in
           case it allocates too much memory. A value of *0* indicates that there is no
           memory limit. **Note: the server will set a maximum value.**
          - **bindVars** (object): key/value pairs representing the bind parameters.
          - **options**: key/value object with extra options for the query.
           **Note: options will be ignored.**
          - **then**: key/value object with actions to apply on the returned query.


        The query details include the query string plus optional query options and
        bind parameters. These values need to be passed in a JSON representation in
        the body of the POST request.


        **HTTP 201**
        *A json document with these Properties is returned:*

        is returned if the result set can be created by the server.

        - **error**: A flag to indicate that an error occurred (*false* in this case)
        - **code**: the HTTP status code
        - **result** (anonymous json object): an array of result documents (might be empty if query has no results)
        - **hasMore**: A boolean indicator whether there are more results
        available for the cursor on the server
        - **count**: the total number of result documents available (only
        available if the query was executed with the *count* attribute set)
        - **id**: id of temporary cursor created on the server (optional, see above)
        - **extra**: an optional JSON object with extra information about the query result
        contained in its *stats* sub-attribute. For data-modification queries, the
        *extra.stats* sub-attribute will contain the number of modified documents and
        the number of documents that could not be modified
        due to an error (if *ignoreErrors* query option is specified)
        - **cached**: a boolean flag indicating whether the query result was served
        from the query cache or not. If the query result is served from the query
        cache, the *extra* return attribute will not contain any *stats* sub-attribute
        and no *profile* sub-attribute.


        **HTTP 400**
        *A json document with these Properties is returned:*

        is returned if the JSON representation is malformed or the query specification is
        missing from the request.
        If the JSON representation is malformed or the query specification is
        missing from the request, the server will respond with *HTTP 400*.
        The body of the response will contain a JSON object with additional error
        details, that will be available in the `details` attribute of an standard
        Altair® IoT Studio™ API error response.
        The error object has the following attributes:

        - **error**: boolean flag to indicate that an error occurred (*true* in this case)
        - **code**: the HTTP status code
        - **errorNum**: the server error number
        - **errorMessage**: a descriptive error message<br>
        If the query specification is complete, the server will process the query. If an
        error occurs during query processing, the server will respond with *HTTP 400*.
        Again, the body of the response will contain details about the error.

        :param req: Request payload.
        :type req: Union[models.PostAPICursor, dict]
        :return: The API response to the request.
        :rtype: Union[models.PostAPICursorResponse, models.ErrorResponse, primitives.NoResponse]
        """
        req_content_types = [
            ("application/json", models.PostAPICursor),
        ]

        resp = self._make_request("POST", req, req_content_types=req_content_types, **kwargs)
        return self._handle_response(resp, [
            (201, "application/json", models.PostAPICursorResponse),
            (400, "application/json", models.ErrorResponse),
            (401, "application/json", models.ErrorResponse),
            (403, "application/json", models.ErrorResponse),
            (404, "application/json", models.ErrorResponse),
            (405, "", primitives.NoResponse),
            (500, "application/json", models.ErrorResponse),
        ])

    def _build_partial_path(self):
        return "/cursor"


class _CursorMethods:
    """
    This class declares and implements the `cursor()` method.
    """

    @overload
    def cursor(self, cursor_id: str) -> Cursor1:
        ...

    @overload
    def cursor(self) -> Cursor2:
        ...

    def cursor(self, cursor_id: str = None):
        if cursor_id is not None :
            return Cursor1(cursor_id)._child_of(self)

        if cursor_id is None:
            return Cursor2()._child_of(self)

        raise ValueError("Invalid parameters")
