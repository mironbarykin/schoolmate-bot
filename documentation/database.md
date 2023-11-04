## Accounts

The `accounts` table stores information about users of the system. The table has the following columns:

* `id`: The telegram's unique identifier for the user.
* `name`: The user's name.
* `access`: The user's access level.

## Approvals

The `approvals` table stores information about requests that need to be approved. The table has the following columns:

* `message_id`: The ID of the message that contains the request.
* `approver_id`: The ID of the user who needs to approve the request.
* `requester_id`: The ID of the user who submitted the request.
