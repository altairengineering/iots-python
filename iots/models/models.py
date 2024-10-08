# generated by datamodel-codegen:
#   filename:  schemas.yaml
#   timestamp: 2024-09-04T15:17:24+00:00

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Union

from pydantic import Extra, Field, conint, constr

from .basemodel import APIBaseModel


class Paging(APIBaseModel):
    next_cursor: Optional[str] = Field(None, example='')
    previous_cursor: Optional[str] = Field(None, example='')


class AnyValue(APIBaseModel):
    __root__: Optional[Union[List, bool, int, float, Dict[str, Any], str]] = Field(
        None, description='Any value - string, number, boolean, array, object or null.'
    )


class Type(Enum):
    boolean = 'boolean'
    integer = 'integer'
    number = 'number'
    string = 'string'
    object = 'object'
    array = 'array'
    null = 'null'


class DataSchema(APIBaseModel):
    class Config:
        extra = Extra.forbid

    field_type: Optional[Union[str, List[str]]] = Field(None, alias='@type')
    const: Optional[Any] = None
    description: Optional[str] = None
    enum: Optional[List] = Field(None, min_items=1, unique_items=True)
    items: Optional[Union[DataSchema, List[DataSchema]]] = None
    maxItems: Optional[conint(ge=0)] = None
    maximum: Optional[float] = None
    minItems: Optional[conint(ge=0)] = None
    minimum: Optional[float] = None
    oneOf: Optional[List[DataSchema]] = None
    properties: Optional[Any] = None
    readOnly: Optional[bool] = None
    required: Optional[List[str]] = None
    title: Optional[str] = None
    type: Optional[Type] = None
    unit: Optional[str] = None


class EmailBody(APIBaseModel):
    html: Optional[str] = Field(
        None,
        description='Body content in HTML format.',
        example='<p>Email <b>body</b> content</p>',
    )
    text: Optional[str] = Field(
        None, description='Body content as plain text.', example='Email body content'
    )


class Error(APIBaseModel):
    details: Optional[Dict[str, Any]] = Field(
        None, description='Key/value object with extra information about the error.'
    )
    message: str = Field(..., example='invalid id')
    status: int = Field(..., example=400)


class ErrorResponse(APIBaseModel):
    error: Optional[Error] = None


class EventCreateRequest1(APIBaseModel):
    data: Optional[AnyValue] = None


class EventCreateRequest(APIBaseModel):
    __root__: Optional[Dict[str, EventCreateRequest1]] = None


class EventValue(APIBaseModel):
    data: Optional[AnyValue] = None
    href: Optional[str] = None
    timestamp: Optional[datetime] = None


class Forbidden(APIBaseModel):
    __root__: Any = Field(..., description='Forbidden')


class ID(APIBaseModel):
    __root__: str = Field(..., example='01FPJGR4TWXHH23EHEKT4HEN6F')


class InteractionAffordance(APIBaseModel):
    field_type: Optional[Union[str, List[str]]] = Field(None, alias='@type')
    description: Optional[str] = None
    title: Optional[str] = None


class Op(Enum):
    add = 'add'
    remove = 'remove'
    replace = 'replace'
    move = 'move'
    copy = 'copy'
    test = 'test'


class JsonPatchOperation(APIBaseModel):
    from_: Optional[str] = Field(
        None,
        alias='from',
        description='The path from which the value will be moved or copied. Required for "move" and "copy" operations.',
    )
    op: Op = Field(..., description='The type of operation to be performed.')
    path: str = Field(
        ...,
        description='The path in the JSON document where the operation will be applied.',
    )
    value: Optional[AnyValue] = Field(
        None,
        description='The new value to be applied. Required for "add", "replace", and "test" operations.',
    )


class Link(APIBaseModel):
    href: Optional[str] = Field(
        None,
        description='Target IRI of a link or submission target of a form.',
        example='https://help.altair.com/altair-iot-studio/index.htm',
    )
    rel: Optional[str] = Field(
        None,
        description='A link relation type identifies the semantics of a link.',
        example='documentation',
    )


class MQTTForm(APIBaseModel):
    description: Optional[str] = Field(None, example='MyCredential')
    enabled: Optional[bool] = Field(None, example=True)
    password: Optional[str] = Field(None, example='MyPa$$word123')
    username: Optional[str] = Field(None, example='myusername')


class MQTTFormGet(APIBaseModel):
    description: Optional[str] = Field(None, example='MyCredential')
    enabled: Optional[bool] = Field(None, example=True)
    password: Optional[str] = Field(None, example='<hidden_secret>')
    username: Optional[str] = Field(None, example='myusername')


class PublishItem(APIBaseModel):
    pattern: Optional[str] = Field(
        None,
        example='altair/collections/my_collection/things/01FWDZKSRZFGDACF4N7E3VSBBZ/data',
    )


class SubscribeItem(APIBaseModel):
    pattern: Optional[str] = Field(
        None,
        example='altair/collections/my_collection/things/01FWDZKSRZFGDACF4N7E3VSBBZ/data',
    )


class Acl(APIBaseModel):
    publish: Optional[List[PublishItem]] = None
    subscribe: Optional[List[SubscribeItem]] = None


class MQTTThingDocumentACL(APIBaseModel):
    acl: Optional[Acl] = None


class MQTTThingForm(MQTTForm):
    pass


class MQTTThingFormGet(MQTTFormGet):
    pass


class MQTTThingsDocument(MQTTThingForm):
    created: Optional[str] = Field(None, example='2022-02-08T14:41:49.270946386+01:00,')
    id: Optional[ID] = None


class ModelBase(APIBaseModel):
    description: Optional[str] = Field(
        None, description='Description of the Model.', example='My Raspberry Pi Model'
    )
    name: constr(regex=r'^[a-zA-Z0-9_:-]{1,26}$') = Field(
        ...,
        description='Name of the Model that will be used as a unique identifier.',
        example='RaspberryPiModel',
    )


class ModelCreate(ModelBase):
    name: constr(regex=r'^[a-zA-Z0-9_:-]{1,26}$') = Field(
        ...,
        description='Name of the Model that will be used as a unique identifier.',
        example='RaspberryPiModel',
    )


class ModelDescription(APIBaseModel):
    name: Optional[str] = Field(
        None, description='Model name.', example='RaspberryPiModel'
    )
    version: Optional[int] = Field(None, description='Version number.', example=1)


class ModelDescriptionCategory(APIBaseModel):
    name: str = Field(..., description='Model name.', example='RaspberryPiModel')
    version: Optional[int] = Field(None, description='Version number.', example=1)


class ModelUpdate(ModelBase):
    name: constr(regex=r'^[a-zA-Z0-9_:-]{1,26}$') = Field(
        ...,
        description='Name of the Model that will be used as a unique identifier.',
        example='RaspberryPiModel',
    )


class Template(APIBaseModel):
    actions: Optional[Dict[str, Any]] = Field(
        None,
        description='Action definitions of the Thing.',
        example={
            'delay': {
                'description': 'Change sending frequency',
                'input': {
                    'properties': {
                        'input': {'maximum': 100, 'minimum': 3, 'type': 'number'}
                    }
                },
                'title': 'Delay',
            }
        },
    )
    description: Optional[str] = Field(
        None,
        description='Description of the Thing.',
        example='My connected Altair® IoT Studio™ device',
    )
    events: Optional[Dict[str, Any]] = Field(
        None,
        description='Event definitions of the Thing.',
        example={
            'highCPU': {
                'data': {'type': 'number', 'unit': 'percent'},
                'description': 'The CPU usage is over 50%',
                'title': 'High CPU',
            }
        },
    )
    links: Optional[List[Dict[str, Any]]] = Field(
        None, description='Links of the Thing.'
    )
    properties: Optional[Dict[str, Any]] = Field(
        None,
        description='Property definitions of the Thing.',
        example={
            'cpu': {
                'description': 'Device CPU usage in percent',
                'readOnly': False,
                'title': 'CPU %',
                'type': 'number',
                'unit': 'percent',
            }
        },
    )
    title: Optional[str] = Field(
        None, description='Name of the Thing.', example='Altair® IoT Studio™ Device'
    )


class ModelVersionBase(APIBaseModel):
    description: Optional[str] = Field(
        None,
        description='Description of the Model-Version.',
        example='Version 1 of RaspberryPiModel',
    )
    template: Optional[Template] = Field(
        None,
        description='Describes the information of a Thing associated to the Model-Version.\n\nIf a Model-Version is applied to a Thing, all defined `template`\nfields that are defined (i.e. those with non-null values) will\nreplace these same fields in the Thing description.\n',
    )
    title: Optional[str] = Field(
        None, description='Name of the Model-Version.', example='Version 1'
    )


class ModelVersionCreate(ModelVersionBase):
    pass


class Then(APIBaseModel):
    error_count: Optional[bool] = Field(
        None, description='The number of results that could not be modified.'
    )
    success_count: Optional[bool] = Field(
        None, description='The number of results that were successfully modified.'
    )


class PostAPICursorResponse(APIBaseModel):
    cached: Optional[bool] = Field(
        None,
        description='A boolean flag indicating whether the query result was served\nfrom the query cache or not. If the query result is served from the query\ncache, the *extra* return attribute will not contain any *stats* sub-attribute\nand no *profile* sub-attribute.\n',
    )
    code: Optional[int] = Field(
        None, description='The HTTP status code of the response from ArangoDB.\n'
    )
    count: Optional[int] = Field(
        None,
        description='The total number of result documents available (only\navailable if the query was executed with the *count* attribute set).\n',
    )
    error: bool = Field(..., description='A flag to indicate that an error occurred.\n')
    extra: Optional[Dict[str, Any]] = Field(
        None,
        description='An optional JSON object with extra information about the query result\ncontained in its *stats* sub-attribute. For data-modification queries, the\n*extra.stats* sub-attribute will contain the number of modified documents and\nthe number of documents that could not be modified\ndue to an error (if *ignoreErrors* query option is specified).\n',
    )
    hasMore: Optional[bool] = Field(
        None,
        description='A boolean indicating whether there are more results\navailable for the cursor on the server.\n',
    )
    id: Optional[str] = Field(
        None,
        description='ID of temporary cursor created on the server (optional, see above).\n',
    )
    result: Optional[List] = Field(
        None,
        description='An array of result documents (might be empty if query has no results).\n',
    )
    then: Optional[Then] = Field(
        None,
        description='Includes information about the operation performed on the query results\n(only applicable if `then` was used in the request).\n',
    )


class Properties(APIBaseModel):
    __root__: Optional[Dict[str, Any]] = None


class Property(APIBaseModel):
    __root__: Optional[Dict[str, Any]] = None


class PropertyAffordance(InteractionAffordance):
    observable: Optional[bool] = None


class PropertyValues(APIBaseModel):
    __root__: Optional[Dict[str, Any]] = None


class ThenOperation(APIBaseModel):
    data: Optional[Any] = Field(
        None,
        description='The data used to modify the resources.',
        example={'update_firmware': True},
    )
    op: Optional[str] = Field(
        None,
        description='Operation type on the resources of the query results. Supported operations:\n  - `update`: Update the resources.\n  - `delete`: Delete the resources.\n',
        example='update',
    )
    resource: Optional[str] = Field(
        None,
        description='Type of resource the operation will be applied to. Supported resources:\n  - `things`: The Thing description of the Things with the returned IDs.\n  - `properties`: The Properties of the Things with the returned IDs.\n',
        example='properties',
    )


class ThenQueryRequest(APIBaseModel):
    then: Optional[ThenOperation] = None


class ThingOAuth2Credentials(APIBaseModel):
    client_id: Optional[str] = Field(
        None,
        description="The Client ID of the Thing's OAuth2 client.",
        example='altair::01GJCPZPVCZKD9GDV4A51NT27H',
    )
    client_secret: Optional[str] = Field(
        None,
        description="The Client secret of the Thing's OAuth2 client.",
        example='MSivCvI71kHEAo0tXY6edIhTsQl12n',
    )


class ThingPatch(APIBaseModel):
    __root__: List[JsonPatchOperation] = Field(
        ...,
        description='A JSON Patch request to apply to a Thing.',
        example=[
            {'op': 'replace', 'path': '/description', 'value': 'Updating my Thing'}
        ],
        title='Thing Patch Request',
    )


class ThingsDeleted(APIBaseModel):
    __root__: List[str] = Field(
        ...,
        description='List of IDs of the deleted Things.',
        example=['01GM38SSQC0X32YQSXZYFJPGGC', '01GM38T332KMGEXJZNB6VYTRBM'],
        title='Things Deleted',
    )


class ThingsPatchItem(APIBaseModel):
    id: Optional[str] = Field(None, description='ID of the Thing.')
    patch: Optional[List[ThingPatch]] = Field(
        None, description='Patch to apply to the Thing.'
    )


class ThingsPatch(APIBaseModel):
    __root__: List[ThingsPatchItem] = Field(
        ...,
        description='A JSON Patch request to apply to multiple Things.',
        example=[
            {
                'id': '01FPSXTMN4CEGX09HF5RQ4RMY6',
                'patch': [
                    {
                        'op': 'replace',
                        'path': '/description',
                        'value': 'Updating my Thing',
                    }
                ],
            }
        ],
        title='Multi-Thing Patch Request',
    )


class Results(APIBaseModel):
    response: Optional[Dict[str, Any]] = None
    status: Optional[int] = None


class ThingsPatchMultiStatus(APIBaseModel):
    has_errors: Optional[List[int]] = Field(
        None, description='List of indexes of the items that have errors.'
    )
    results: Optional[Results] = Field(
        None, description='List of results for each item.'
    )


class ActionAffordance(InteractionAffordance):
    idempotent: Optional[bool] = None
    input: Optional[DataSchema] = None
    output: Optional[DataSchema] = None
    safe: Optional[bool] = None


class ActionCreateRequest1(APIBaseModel):
    input: Optional[AnyValue] = None


class ActionCreateRequest(APIBaseModel):
    __root__: Optional[Dict[str, ActionCreateRequest1]] = None


class ActionUpdateRequest1(APIBaseModel):
    output: Optional[AnyValue] = None
    status: Optional[str] = None


class ActionUpdateRequest(APIBaseModel):
    __root__: Optional[Dict[str, ActionUpdateRequest1]] = None


class ActionValue(APIBaseModel):
    href: Optional[str] = None
    input: Optional[AnyValue] = None
    status: Optional[str] = None
    timeCompleted: Optional[datetime] = None
    timeRequested: Optional[datetime] = None


class CategoryBase(APIBaseModel):
    description: Optional[str] = Field(
        None, description='The description of the Category.', example='My category'
    )
    model: Optional[ModelDescriptionCategory] = Field(
        None,
        description='The Model or Model and Version that all the Things in the Category\nmust match in order to belong to it.\n',
    )
    name: Optional[constr(regex=r'^[a-zA-Z0-9_:-]{1,26}$')] = Field(
        None,
        description='Name of the Category that will be used as a unique identifier.',
        example='ElectronicBoards',
    )


class CategoryCreate(CategoryBase):
    name: constr(regex=r'^[a-zA-Z0-9_:-]{1,26}$') = Field(
        ...,
        description='Name of the Category that will be used as a unique identifier.',
        example='ElectronicBoards',
    )


class CategoryUpdate(CategoryBase):
    name: constr(regex=r'^[a-zA-Z0-9_:-]{1,26}$') = Field(
        ...,
        description='Name of the Category that will be used as a unique identifier.',
        example='ElectronicBoards',
    )


class Email(APIBaseModel):
    bcc: Optional[List[str]] = Field(
        None,
        description='Recipient(s) of the email as BCC (blind carbon copy).',
        example=['marymajor@altair.com', 'richardmiles@altair.com'],
    )
    body: Optional[EmailBody] = Field(None, description='Body of the email.')
    cc: Optional[List[str]] = Field(
        None,
        description='Recipient(s) of the email as CC (carbon copy).',
        example=['judydoe@altair.com', 'johnstiles@altair.com'],
    )
    subject: Optional[str] = Field(
        None, description='Subject of the email.', example='Email Subject Example'
    )
    to: List[str] = Field(
        ...,
        description='Main recipient(s) of the email.',
        example=['johndoe@altair.com', 'janedoe@altair.com'],
    )


class EventAffordance(InteractionAffordance):
    cancellation: Optional[DataSchema] = None
    data: Optional[DataSchema] = None
    subscription: Optional[DataSchema] = None


class EventResponse(APIBaseModel):
    __root__: Optional[Dict[str, EventValue]] = None


class MQTTCategoryForm(MQTTForm):
    collection_name: Optional[str] = Field(None, example='MyCollection')


class MQTTThingDocument(MQTTThingForm):
    created: Optional[str] = Field(None, example='2022-02-08T14:41:49.270946386+01:00,')
    id: Optional[ID] = None
    topics: Optional[MQTTThingDocumentACL] = None


class MQTTThingDocumentGet(MQTTThingFormGet):
    created: Optional[str] = Field(None, example='2022-02-08T14:41:49.270946386+01:00,')
    id: Optional[ID] = None
    topics: Optional[MQTTThingDocumentACL] = None


class MQTTThingsDocumentList(APIBaseModel):
    data: Optional[List[MQTTThingDocument]] = None
    paging: Optional[Paging] = None


class Model(ModelBase):
    id: Optional[str] = Field(None, example='01FPT3MJBRBMA5462PEE57FRKB')
    created: Optional[datetime] = Field(None, example='2021-11-17T10:08:31Z')
    modified: Optional[datetime] = Field(None, example='2021-11-17T10:08:31Z')


class ModelList(APIBaseModel):
    data: Optional[List[Model]] = None
    paging: Optional[Paging] = None


class ModelVersion(ModelVersionBase):
    version: Optional[int] = Field(None, example=1)
    created: Optional[datetime] = Field(None, example='2021-11-23T21:11:37Z')


class ModelVersionList(APIBaseModel):
    data: Optional[List[ModelVersion]] = None
    paging: Optional[Paging] = None


class PostAPICursor(APIBaseModel):
    batchSize: Optional[int] = Field(
        None,
        description='Maximum number of result documents to be transferred from\nthe server to the client in one roundtrip. If this attribute is\nnot set, a server-controlled default value will be used. A *batchSize* value of\n*0* is disallowed.\n',
    )
    bindVars: Optional[List[Dict[str, Any]]] = Field(
        None, description='Key/value pairs representing the bind parameters.\n'
    )
    cache: Optional[bool] = Field(
        None,
        description='Flag to determine whether the AQL query results cache\nshall be used. If set to *false*, then any query cache lookup will be skipped\nfor the query. If set to *true*, it will lead to the query cache being checked\nfor the query if the query cache mode is either *on* or *demand*.\n',
    )
    count: Optional[bool] = Field(
        None,
        description='Indicates whether the number of documents in the result set should be returned in\nthe "count" attribute of the result.\nCalculating the "count" attribute might have a performance impact for some queries\nin the future so this option is turned off by default, and "count"\nis only returned when requested.\n',
    )
    memoryLimit: Optional[int] = Field(
        None,
        description='The maximum number of memory (measured in bytes) that the query is allowed to\nuse. If set, then the query will fail with error "resource limit exceeded" in\ncase it allocates too much memory. A value of *0* indicates that there is no\nmemory limit.\n',
    )
    options: Optional[Dict[str, Any]] = Field(
        None, description='This attribute is currently ignored.'
    )
    query: str = Field(..., description='Contains the query string to be executed\n')
    then: Optional[ThenOperation] = None
    ttl: Optional[int] = Field(
        None,
        description='The time-to-live for the cursor (in seconds). If the result set is small enough\n(less than or equal to `batchSize`) then results are returned right away.\nOtherwise they are stored in memory and will be accessible via the cursor with\nrespect to the `ttl`. The cursor will be removed on the server automatically\nafter the specified amount of time. This is useful to ensure garbage collection\nof cursors that are not fully fetched by clients. If not set, a server-defined\nvalue will be used (default: 30 seconds).\n',
    )


class PropertyHistoryValue(APIBaseModel):
    at: datetime = Field(
        ...,
        description='Date and time the values were recorded.',
        example='2022-08-22T13:10:00Z',
    )
    properties: PropertyValues


class PropertyHistoryValueList(APIBaseModel):
    data: Optional[List[PropertyHistoryValue]] = None
    paging: Optional[Paging] = None


class PropertyHistoryValues(APIBaseModel):
    __root__: List[PropertyHistoryValue] = Field(
        ...,
        description='List of historical Property values.',
        example=[
            {
                'at': '2022-08-22T13:10:00Z',
                'properties': {'cpu': 43, 'disk': 19, 'memory': 27},
            },
            {'at': '2022-08-22T13:09:00Z', 'properties': {'cpu': 87, 'memory': 69}},
            {'at': '2022-08-22T13:08:30Z', 'properties': {'disk': 17}},
        ],
        title='Property History Values',
    )


class ThingBase(APIBaseModel):
    field_context: Optional[str] = Field(
        None,
        alias='@context',
        description='JSON-LD keyword to define short-hand names called terms that are\nused throughout a TD document.\n',
        example='context',
    )
    field_type: Optional[Union[str, List[str]]] = Field(
        None,
        alias='@type',
        description='JSON-LD keyword to label the object with semantic tags (or types).\n',
        example=['Light', 'OnOffSwitch'],
    )
    actions: Optional[Dict[str, ActionAffordance]] = Field(
        None,
        description='Action descriptions of the Thing.',
        example={
            'delay': {
                'description': 'Change sending frequency',
                'input': {
                    'properties': {
                        'input': {'maximum': 100, 'minimum': 3, 'type': 'number'}
                    }
                },
                'title': 'Delay',
            },
            'reboot': {'description': 'Reboot device', 'title': 'Reboot'},
        },
    )
    description: Optional[str] = Field(
        None,
        description='Description of the Thing.',
        example='My connected Altair® IoT Studio™ device',
    )
    events: Optional[Dict[str, EventAffordance]] = Field(
        None,
        description='Event descriptions of the Thing.',
        example={
            'highCPU': {
                'data': {'type': 'number', 'unit': 'percent'},
                'description': 'The CPU usage is over 50%',
                'title': 'High CPU',
            }
        },
    )
    links: Optional[List[Link]] = Field(
        None,
        description='Provides Web links to arbitrary resources that relate to the Thing.\nAny link to other Thing in the same space will create a graph\nrelationship between the two Things.\n',
        example=[
            {
                'href': 'https://help.altair.com/altair-iot-studio/index.htm',
                'rel': 'documentation',
            },
            {
                'href': 'https://api.swx.altairone.com/spaces/space01/things/01FPSXTMN4CEGX09HF5RQ4RMY6',
                'rel': 'parent',
            },
        ],
    )
    model: Optional[ModelDescription] = Field(
        None, description='Model and Version applied to the Thing.'
    )
    properties: Optional[Dict[str, PropertyAffordance]] = Field(
        None,
        description='Property descriptions of the Thing.',
        example={
            'cpu': {
                'description': 'Device CPU usage in percent',
                'readOnly': False,
                'title': 'CPU %',
                'type': 'number',
                'unit': 'percent',
            },
            'disk': {
                'description': 'Device Disk usage in percent',
                'readOnly': False,
                'title': 'Disk %',
                'type': 'number',
                'unit': 'percent',
            },
            'memory': {
                'description': 'Device Memory usage in percent',
                'readOnly': False,
                'title': 'Memory %',
                'type': 'number',
                'unit': 'percent',
            },
        },
    )
    status: Optional[PropertyValues] = None
    title: Optional[str] = Field(
        None, description='Name of the Thing.', example='Altair® IoT Studio™ Device'
    )


class ThingCategory(ThingBase):
    client_id: Optional[str] = Field(
        None,
        description='The ID of the OAuth2 client of this Thing. This field will not\nbe included in the response if the client has not been setup.\n',
        example='space01::01FPSXTMN4CEGX09HF5RQ4RMY6',
    )
    id: Optional[str] = Field(
        None,
        example='https://api.swx.altairone.com/spaces/space01/categories/category1/things/01FPSXTMN4CEGX09HF5RQ4RMY6',
    )
    uid: Optional[str] = Field(None, example='01FPSXTMN4CEGX09HF5RQ4RMY6')
    created: Optional[datetime] = Field(None, example='2021-12-13T09:38:11Z')
    modified: Optional[datetime] = Field(None, example='2021-12-13T09:38:11Z')


class ThingCategoryCreate(ThingBase):
    pass


class ThingCategoryList(APIBaseModel):
    data: Optional[List[ThingCategory]] = None
    paging: Optional[Paging] = None


class ThingCategoryUpdate(ThingBase):
    id: Optional[str] = Field(
        None,
        example='https://api.swx.altairone.com/spaces/space01/categories/category1/things/01FPSXTMN4CEGX09HF5RQ4RMY6',
    )
    uid: Optional[str] = Field(None, example='01FPSXTMN4CEGX09HF5RQ4RMY6')


class ThingCreate(ThingBase):
    categories: Optional[List[str]] = Field(
        None,
        description='List of Category names the Thing belongs to.',
        example=['category1', 'category2'],
    )


class ThingUpdate(ThingBase):
    id: Optional[str] = Field(
        None,
        example='https://api.swx.altairone.com/spaces/space01/things/01FPSXTMN4CEGX09HF5RQ4RMY6',
    )
    uid: Optional[str] = Field(None, example='01FPSXTMN4CEGX09HF5RQ4RMY6')
    categories: Optional[List[str]] = Field(
        None,
        description='List of Category names the Thing belongs to.',
        example=['category1', 'category2'],
    )


class ActionResponse(APIBaseModel):
    __root__: Optional[Dict[str, ActionValue]] = None


class Category(CategoryBase):
    created: Optional[datetime] = Field(None, example='2021-11-17T03:15:40Z')
    modified: Optional[datetime] = Field(None, example='2021-11-17T03:15:40Z')


class CategoryList(APIBaseModel):
    data: Optional[List[Category]] = None
    paging: Optional[Paging] = None


class CreateCategoryPropertiesHistoryValuesRequest(APIBaseModel):
    __root__: Union[PropertyHistoryValue, PropertyHistoryValues]


class CreateCategoryPropertyHistoryValuesRequest(APIBaseModel):
    __root__: Union[PropertyHistoryValue, PropertyHistoryValues]


class CreatePropertiesHistoryValuesRequest(APIBaseModel):
    __root__: Union[PropertyHistoryValue, PropertyHistoryValues]


class CreatePropertyHistoryValuesRequest(APIBaseModel):
    __root__: Union[PropertyHistoryValue, PropertyHistoryValues]


class EventListResponse(APIBaseModel):
    data: Optional[List[EventResponse]] = Field(
        None,
        example=[
            {
                'highCPU': {
                    'data': 61,
                    'href': '/spaces/altair/things/01FPSXTMN4CEGX09HF5RQ4RMY6/events/highCPU/01EDCEZDTJX50SQTCJST5EW5NX',
                    'timestamp': '2020-04-02 15:22:37+0000',
                }
            },
            {
                'highCPU': {
                    'data': 85,
                    'href': '/spaces/altair/things/01FPSXTMN4CEGX09HF5RQ4RMY6/events/highCPU/01EDCGYKV4YQ1CY3QHHSX8J843',
                    'timestamp': '2020-04-02 15:26:42+0000',
                }
            },
            {
                'lowDiskSpace': {
                    'data': 95,
                    'href': '/spaces/altair/things/01FPSXTMN4CEGX09HF5RQ4RMY6/events/lowDiskSpace/01GPX7BR5X3YT5Y65ZMT24YT1N',
                    'timestamp': '2020-04-03 07:12:55+0000',
                }
            },
        ],
    )
    paging: Optional[Paging] = None


class MQTTCategoryDocument(MQTTCategoryForm):
    created: Optional[str] = Field(None, example='2022-02-08T14:41:49.270946386+01:00,')
    id: Optional[ID] = None


class Resource(APIBaseModel):
    data: Optional[Union[ActionResponse, EventResponse, PropertyHistoryValues]] = Field(
        None, description='Historical data returned from Things.'
    )
    thing_id: Optional[str] = Field(
        None, description='Indicates the Thing ID', example='01FPSXTMN4CEGX09HF5RQ4RMY6'
    )


class ResourceList(APIBaseModel):
    data: Optional[List[Resource]] = None
    paging: Optional[Paging] = None


class Thing(ThingBase):
    categories: Optional[List[str]] = Field(
        None,
        description='List of Category names the Thing belongs to.',
        example=['category1', 'category2'],
    )
    client_id: Optional[str] = Field(
        None,
        description='The ID of the OAuth2 client of this Thing. This field will not\nbe included in the response if the client has not been setup.\n',
        example='space01::01FPSXTMN4CEGX09HF5RQ4RMY6',
    )
    id: Optional[str] = Field(
        None,
        example='https://api.swx.altairone.com/spaces/space01/things/01FPSXTMN4CEGX09HF5RQ4RMY6',
    )
    uid: Optional[str] = Field(None, example='01FPSXTMN4CEGX09HF5RQ4RMY6')
    created: Optional[datetime] = Field(None, example='2021-12-13T09:38:11Z')
    modified: Optional[datetime] = Field(None, example='2021-12-13T09:38:11Z')


class ThingList(APIBaseModel):
    data: Optional[List[Thing]] = None
    paging: Optional[Paging] = None


class ActionListResponse(APIBaseModel):
    data: Optional[List[ActionResponse]] = Field(
        None,
        example=[
            {
                'delay': {
                    'href': '/spaces/altair/things/01FPSXTMN4CEGX09HF5RQ4RMY6/actions/delay/01EDCAQE78A7CP6REXV5J8BAKR',
                    'input': {'delay': 5},
                    'status': 'pending',
                    'timeRequested': '2022-06-02 15:37:46+0000',
                }
            },
            {
                'delay': {
                    'href': '/spaces/altair/things/01FPSXTMN4CEGX09HF5RQ4RMY6/actions/delay/01EDCB9FMD0Q3QR0YV4TWY4S3E',
                    'input': {'delay': 7},
                    'status': 'pending',
                    'timeRequested': '2022-06-02 15:39:54+0000',
                }
            },
            {
                'reboot': {
                    'href': '/spaces/altair/things/01FPSXTMN4CEGX09HF5RQ4RMY6/actions/delay/01EDCCZYATJW1Z3D4T4BA4S2QH',
                    'status': 'pending',
                    'timeRequested': '2022-06-02 15:56:12+0000',
                }
            },
        ],
    )
    paging: Optional[Paging] = None


DataSchema.update_forward_refs()
