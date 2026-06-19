# AGENTS.md

## Project Overview

### Project Name

**T4 Gate Keeper**

### Technical Stack

* Framework: Odoo 19
* Language: Python 3
* Database: PostgreSQL
* Frontend: Odoo XML Views, JavaScript (when required)
* Module Name: `t4_gate_keeper`

### Purpose

T4 Gate Keeper is a backend system responsible for managing physical access control infrastructure.

The system manages:

* Controllers
* Devices
* Company-based ownership and visibility

The project is currently in the MVP phase and focuses on controller and device management.

---

# Core Business Concepts

## Controller

In this project, a **Controller** is a physical hardware device.

It is **NOT** an Odoo controller and **NOT** an MVC controller.

Responsibilities:

* Acts as an intermediate gateway.
* Communicates with multiple devices.
* Collects data from devices.
* Sends data back to the server.
* Receives commands from the server and forwards them to devices.

Whenever the term **Controller** appears in the codebase, documentation, comments, or generated code, it refers to the physical controller hardware.

---

## Device

A Device is a hardware endpoint managed by a Controller.

Examples:

* Door reader
* RFID reader
* Fingerprint scanner
* Face recognition terminal
* Access sensor

A Device must always belong to a Controller.

---

# Multi-Company Architecture

The system is company-aware.

Current business rule:

* Each company can only view its own Controllers.
* Each Controller belongs to exactly one company.
* Devices inherit visibility from their Controller.
* Users should only access records associated with their company.

Expected navigation flow:

Company
→ Controllers
→ Devices

When opening a Controller record, users should be able to view Devices managed by that Controller.

---

# Naming Conventions

## Model Names

All business models MUST start with:

```python
t4.gate_keeper
```

Examples:

```python
t4.gate_keeper.controller
t4.gate_keeper.device
t4.gate_keeper.access_log
t4.gate_keeper.command
```

Do NOT create models outside this namespace unless explicitly approved.

---

## Python Classes

Use descriptive class names.

Examples:

```python
class GateKeeperController(models.Model):
    ...
```

```python
class GateKeeperDevice(models.Model):
    ...
```

---

## XML IDs

Use module-prefixed XML IDs.

Examples:

```xml
t4_gate_keeper.view_controller_tree
t4_gate_keeper.view_controller_form
t4_gate_keeper.action_controller
t4_gate_keeper.menu_controller
```

---

## Files

Use snake_case naming.

Examples:

```text
controller.py
device.py
controller_views.xml
device_views.xml
security.xml
ir.model.access.csv
```

---

# Development Rules

## Approval Required

The AI assistant MUST NOT:

* Modify existing architecture.
* Rename models.
* Rename fields.
* Modify security rules.
* Modify record rules.
* Modify access rights.
* Create new dependencies.
* Change manifest configuration.
* Change database structure.

without explicit approval from the developer.

When a modification affects architecture or existing behavior, the assistant must first explain:

1. What will change.
2. Why it is needed.
3. Potential side effects.

Implementation should only proceed after approval.

---

## Backward Compatibility

All generated code must preserve existing functionality unless the developer explicitly requests breaking changes.

Avoid introducing changes that require data migration unless approved.

---

## Minimal Changes Principle

When fixing bugs:

* Prefer the smallest possible change.
* Avoid refactoring unrelated code.
* Avoid changing coding style in untouched areas.
* Avoid moving files unless necessary.

---

# Language Rules

## Source Code

All generated code must be written in English.

Including:

* Variable names
* Class names
* Method names
* Comments
* Docstrings
* Error messages
* Log messages

Example:

```python
raise ValidationError(_("Controller is offline"))
```

---

## Translation

Every user-facing string must be translatable.

Use:

```python
from odoo import _
```

Example:

```python
_("Controller is offline")
```

An equivalent Vietnamese translation must be provided through i18n files.

Expected:

```text
i18n/
└── vi.po
```

No hardcoded Vietnamese text inside Python source code.

---

# Odoo Development Standards

## ORM First

Always use the Odoo ORM.

Preferred:

```python
self.env['t4.gate_keeper.device'].search(...)
```

Avoid direct SQL unless:

* Performance issue is proven.
* ORM cannot solve the problem.

---

## Security

Never use:

```python
sudo()
```

unless explicitly justified.

When using `sudo()`, document the reason.

---

## Record Rules

Multi-company rules must be respected.

Generated code should not bypass company restrictions.

---

## Logging

Use logging for important operations.

Example:

```python
import logging

_logger = logging.getLogger(__name__)
```

Avoid excessive logging.

Do not log sensitive information.

---

# View Standards

## Tree Views

List views should display:

* Name
* Company
* Status
* Create Date

when applicable.

---

## Form Views

Group fields logically.

Example:

* General Information
* Connection Information
* Hardware Information
* Audit Information

---

# Data Integrity

Use:

* required=True
* SQL constraints
* Python constraints

where appropriate.

Avoid storing duplicated information.

Use relations whenever possible.

---

# Testing Expectations

New features should include:

* Security validation
* Multi-company validation
* Business rule validation

Generated code should not assume administrator access.

---

# Documentation

Every new model should contain:

```python
_name
_description
```

Example:

```python
_name = "t4.gate_keeper.controller"
_description = "Gate Keeper Controller"
```

Complex business logic should include concise comments.

---

# MVP Scope

Current MVP includes:

* Controller Management
* Device Management
* Company Ownership
* Controller → Device Relationship

Features outside MVP should not be implemented unless requested.

Examples:

* Attendance
* Visitor Management
* Access Scheduling
* Facial Recognition
* Mobile Applications
* Real-time Monitoring Dashboards

These features may be introduced later and should not influence current design decisions.

---

# AI Assistant Behavior

Before generating code:

1. Understand the existing architecture.
2. Reuse existing patterns.
3. Preserve backward compatibility.
4. Respect multi-company rules.
5. Ask for approval before structural changes.

When uncertain, prefer asking questions rather than making architectural assumptions.

The AI assistant acts as a contributor, not an architect. Final architectural decisions belong to the developer.


# API Development Standards

## API Framework

This project is built on top of the internal framework:

```python
odoo.addons.t4_coreapi
```

The `t4_coreapi` module is responsible for:

* Endpoint registration
* Request routing
* Request parsing
* Response handling
* API lifecycle management

Developers must follow the conventions defined by this framework.

Do not create custom HTTP controllers unless explicitly approved.

Preferred approach is always to use the API abstraction provided by `t4_coreapi`.

---

## Endpoint Declaration

Endpoints must be declared using the decorator:

```python
from odoo.addons.t4_coreapi.utils import endpoint
```

Example:

```python
@endpoint(name="Testing")
def test(self):
    pass
```

Do not manually expose routes when the endpoint decorator can be used.

---

## Request Data Access

Request data must be obtained through helper functions provided by `t4_coreapi`.

```python
from odoo.addons.t4_coreapi.utils import (
    get_body,
    get_params,
)
```

### Request Body

```python
body = get_body(self.env.context)
```

Used for:

* POST payload
* JSON payload
* Request body content

Example:

```python
controller_id = get_body(self.env.context).get("controller_id")
```

---

### Query Parameters

```python
params = get_params(self.env.context)
```

Used for:

* URL parameters
* Query string values

Example:

```python
device_id = get_params(self.env.context).get("device_id")
```

---

## Standard Endpoint Example

```python
from odoo import models
from odoo.addons.t4_coreapi.utils import (
    endpoint,
    get_body,
)

import logging

_logger = logging.getLogger(__name__)


class GateKeeperController(models.Model):
    _name = "t4.gate_keeper.controller"
    _description = "Gate Keeper Controller"

    @endpoint(name="Testing")
    def test(self):
        controller_name = get_body(self.env.context).get(
            "controller_id"
        )

        _logger.warning(
            "CONTROLLER: %s",
            controller_name
        )

        if controller_name:
            self.create({
                "controller_name": controller_name
            })
```

---

## Endpoint Naming Convention

Endpoint names should:

* Be descriptive.
* Use English.
* Represent business actions.
* Remain stable after deployment.

Good examples:

```text
ControllerHeartbeat
ControllerRegister
DeviceSync
DeviceStatus
DeviceEvent
AccessLogUpload
```

Avoid:

```text
Test
Test1
ABC
DemoEndpoint
```

unless used temporarily during development.

---

## API Business Logic

Business logic should remain inside models.

Avoid:

* Direct SQL
* Controller-style procedural code
* Massive endpoint methods

Endpoint methods should:

1. Read request data.
2. Validate request data.
3. Call business methods.
4. Return response.

Example:

```python
@endpoint(name="ControllerHeartbeat")
def controller_heartbeat(self):
    body = get_body(self.env.context)

    return self._process_heartbeat(body)
```

---

## Validation Rules

All endpoint inputs should be validated.

Required fields:

```python
controller_id
device_id
company_id
```

must be checked before processing.

Do not assume external hardware sends valid data.

---

## Logging Rules

Incoming requests may be logged for troubleshooting.

Never log:

* Passwords
* Access tokens
* Authentication secrets
* Sensitive biometric data

Allowed:

```python
_logger.info(
    "Heartbeat received from controller %s",
    controller_id
)
```

---

## Error Handling

Never expose Python tracebacks to API consumers.

Use business-friendly error messages.

Bad:

```python
KeyError: controller_id
```

Good:

```python
{
    "success": false,
    "message": "Controller identifier is required."
}
```

---

## Gate Keeper API Philosophy

The T4 Gate Keeper module should not be responsible for:

* HTTP routing
* Request parsing
* Generic API infrastructure

Those responsibilities belong to `t4_coreapi`.

The responsibility of `t4_gate_keeper` is only:

* Controller management
* Device management
* Access-control business logic
* Hardware communication workflows
* Company-based data ownership

```
```
