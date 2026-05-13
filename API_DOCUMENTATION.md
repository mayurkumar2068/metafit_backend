# MetaFit Backend — API Documentation

**Base URL:** `http://127.0.0.1:8000`  
**Swagger UI:** `http://127.0.0.1:8000/swagger/`  
**Auth:** All APIs (except Auth module) require `Authorization: Bearer <access_token>`

---

## App Flow

```
App Open → Token Check → Login/Register → OTP → Onboarding (new) → Home Dashboard
```

| Step | API | When |
|------|-----|------|
| 1 | `POST /api/v1/auth/check-user` | User enters mobile number |
| 2 | `POST /api/v1/auth/send-otp` | After check-user |
| 3 | `POST /api/v1/auth/verify-otp` | User enters OTP → tokens issued |
| 4 | `POST /api/v1/onboarding/profile` | New users only (after first login) |
| 5 | `GET /api/v1/dashboard/home` | Home screen loads |
| 6 | `POST /api/v1/auth/refresh` | When access token expires |

---

## Module 1: Auth (Public — No token required)

### 1.1 Check User

```
POST /api/v1/auth/check-user
```

**Request:**

```json
{
  "mobile_number": "9876543210"
}
```

**Response 200:**

```json
{
  "mobile_number": "9876543210",
  "is_new_user": true,
  "auth_mode": "register",
  "otp_required": true
}
```

| Field | Type | Description |
|-------|------|-------------|
| `is_new_user` | boolean | `true` = not registered, `false` = existing |
| `auth_mode` | string | `"register"` or `"login"` |

---

### 1.2 Send OTP

```
POST /api/v1/auth/send-otp
```

**Request:**

```json
{
  "mobile_number": "9876543210"
}
```

**Response 200:**

```json
{
  "mobile_number": "9876543210",
  "otp_required": true,
  "otp_sent": true,
  "expires_in_seconds": 300,
  "debug_otp": "482917"
}
```

> `debug_otp` is dev-only. Will be removed in production (SMS integration).

---

### 1.3 Verify OTP

```
POST /api/v1/auth/verify-otp
```

**Request:**

```json
{
  "mobile_number": "9876543210",
  "otp": "482917",
  "full_name": "Mayur Bobade",
  "email": "mayur@example.com"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `mobile_number` | string | Yes | |
| `otp` | string (6 digits) | Yes | From send-otp |
| `full_name` | string | Yes | User's name |
| `email` | string | No | Optional email |

**Response 200:**

```json
{
  "is_new_user": true,
  "auth_mode": "register",
  "otp_verified": true,
  "user": {
    "id": 1,
    "mobile_number": "9876543210",
    "email": "mayur@example.com",
    "full_name": "Mayur Bobade"
  },
  "tokens": {
    "access": "<jwt-access-token>",
    "refresh": "<jwt-refresh-token>"
  }
}
```

**Error 400:**

```json
{ "otp": ["Invalid OTP"] }
{ "otp": ["OTP expired or not requested"] }
```

---

### 1.4 Refresh Token

```
POST /api/v1/auth/refresh
```

**Request:**

```json
{
  "refresh": "<jwt-refresh-token>"
}
```

**Response 200:**

```json
{
  "access": "<new-access-token>",
  "refresh": "<new-refresh-token>"
}
```

> Old refresh token is blacklisted after use (rotation enabled).

---

### 1.5 Login (Legacy)

```
POST /api/v1/auth/login
```

**Request:**

```json
{
  "mobile_number": "9876543210",
  "full_name": "Mayur Bobade",
  "email": "mayur@example.com"
}
```

Same response as verify-otp. Use verify-otp flow instead for production.

---

## Module 2: Onboarding (Bearer token required)

### 2.1 Create Onboarding Profile

```
POST /api/v1/onboarding/profile
```

**Request:**

```json
{
  "age": 28,
  "gender": "male",
  "height_cm": 175.0,
  "weight_kg": 72.5,
  "goal": "weight_loss",
  "activity_level": "moderate",
  "medical_conditions": ["diabetes", "thyroid"],
  "dietary_preference": "vegetarian"
}
```

| Field | Type | Required | Options |
|-------|------|----------|---------|
| `age` | integer | Yes | |
| `gender` | string | Yes | `male`, `female`, `other` |
| `height_cm` | decimal | Yes | |
| `weight_kg` | decimal | Yes | |
| `goal` | string | Yes | `weight_loss`, `muscle_gain`, `maintenance`, `general_health` |
| `activity_level` | string | Yes | `sedentary`, `light`, `moderate`, `active`, `very_active` |
| `medical_conditions` | list | No | Array of strings |
| `dietary_preference` | string | No | `vegetarian`, `vegan`, `non_vegetarian`, `eggetarian` |

**Response 201:**

```json
{
  "id": 1,
  "user": {
    "id": 1,
    "mobile_number": "9876543210",
    "email": "mayur@example.com",
    "full_name": "Mayur Bobade"
  },
  "onboarding_complete": true,
  "age": 28,
  "gender": "male",
  "height_cm": 175.0,
  "weight_kg": 72.5,
  "goal": "weight_loss",
  "activity_level": "moderate",
  "medical_conditions": ["diabetes", "thyroid"],
  "dietary_preference": "vegetarian",
  "created_at": "2026-05-12T06:00:00Z",
  "updated_at": "2026-05-12T06:00:00Z"
}
```

**Error 400:** `"Onboarding profile already exists. Use PATCH to update."`

---

### 2.2 Get Onboarding Profile

```
GET /api/v1/onboarding/profile/me
```

**Response 200:** Same as above.  
**Response 404:** `{ "detail": "Onboarding not completed" }`

---

### 2.3 Update Onboarding Profile

```
PATCH /api/v1/onboarding/profile/me
```

**Request (partial):**

```json
{
  "weight_kg": 70.0,
  "goal": "muscle_gain"
}
```

---

## Module 3: Dashboard (Bearer token required)

### 3.1 Home Dashboard

```
GET /api/v1/dashboard/home
```

**Response 200:**

```json
{
  "user": {
    "full_name": "Mayur Bobade",
    "streak_days": 12
  },
  "today_checkin": {
    "id": 45,
    "date": "2026-05-12",
    "weight_kg": 71.8,
    "mood": "good",
    "energy_level": 7,
    "sleep_hours": 7.5,
    "water_litres": 3.0,
    "steps": 8500,
    "notes": ""
  },
  "active_protocol": {
    "id": 1,
    "name": "Fat Loss Phase 1",
    "status": "active",
    "day_number": 12,
    "total_days": 30
  },
  "recent_insights": [
    {
      "id": 5,
      "title": "Sleep improving trend",
      "body": "Your average sleep increased by 0.5h",
      "category": "sleep",
      "severity": "positive"
    }
  ]
}
```

> `today_checkin` = `null` if not submitted today.  
> `active_protocol` = `null` if none active.

---

## Module 4: Daily Check-ins (Bearer token required)

### 4.1 Create Check-in

```
POST /api/v1/checkins/
```

**Request:**

```json
{
  "date": "2026-05-12",
  "weight_kg": 71.8,
  "mood": "good",
  "energy_level": 7,
  "sleep_hours": 7.5,
  "water_litres": 3.0,
  "steps": 8500,
  "notes": "Felt great after workout"
}
```

| Field | Type | Required | Options / Notes |
|-------|------|----------|-----------------|
| `date` | date | Yes | `YYYY-MM-DD` |
| `mood` | string | Yes | `great`, `good`, `okay`, `bad`, `terrible` |
| `energy_level` | integer | Yes | 1-10 |
| `weight_kg` | decimal | No | |
| `sleep_hours` | decimal | No | |
| `water_litres` | decimal | No | |
| `steps` | integer | No | |
| `notes` | string | No | |

**Response 201:** Created check-in object.  
**Error 400:** `"Check-in already exists for this date."`

---

### 4.2 List Check-ins

```
GET /api/v1/checkins/?page=1&page_size=10
GET /api/v1/checkins/?from_date=2026-05-01&to_date=2026-05-12
```

**Response 200:**

```json
{
  "count": 45,
  "page": 1,
  "page_size": 10,
  "results": [ { ... }, { ... } ]
}
```

---

### 4.3 Get Check-in Detail

```
GET /api/v1/checkins/{id}
```

---

### 4.4 Update Check-in

```
PATCH /api/v1/checkins/{id}
```

**Request (partial):**

```json
{ "weight_kg": 72.0, "notes": "Updated" }
```

---

## Module 5: Progress (Bearer token required)

### 5.1 Progress Summary

```
GET /api/v1/progress/summary
```

**Response 200:**

```json
{
  "total_checkins": 45,
  "streak_days": 12,
  "weight_start_kg": 75.0,
  "weight_current_kg": 71.8,
  "weight_change_kg": -3.2,
  "avg_sleep_hours": 7.2,
  "avg_energy_level": 6.8,
  "avg_water_litres": 2.8
}
```

---

### 5.2 Progress Chart Data

```
GET /api/v1/progress/chart?metric=weight&period=30d
```

| Param | Options |
|-------|---------|
| `metric` | `weight`, `sleep`, `energy`, `water`, `steps` |
| `period` | `7d`, `30d`, `90d` |

**Response 200:**

```json
{
  "metric": "weight",
  "period": "30d",
  "data": [
    { "date": "2026-04-12", "value": 75.0 },
    { "date": "2026-04-13", "value": 74.8 }
  ]
}
```

---

## Module 6: Insights (Bearer token required)

### 6.1 List Insights

```
GET /api/v1/insights/?page=1&page_size=10
GET /api/v1/insights/?category=sleep
```

| Param | Options |
|-------|---------|
| `category` | `weight`, `sleep`, `energy`, `water`, `mood`, `general` |

**Response 200:**

```json
{
  "count": 8,
  "page": 1,
  "page_size": 10,
  "results": [
    {
      "id": 5,
      "title": "Sleep improving trend",
      "body": "Your average sleep increased by 0.5h over the last 7 days.",
      "category": "sleep",
      "severity": "positive",
      "created_at": "2026-05-12T06:00:00Z"
    }
  ]
}
```

---

## Module 7: Protocols (Bearer token required)

### 7.1 List Protocols

```
GET /api/v1/protocols/
```

---

### 7.2 Create Protocol

```
POST /api/v1/protocols/
```

**Request:**

```json
{
  "name": "Fat Loss Phase 1",
  "description": "30-day fat loss protocol",
  "start_date": "2026-05-01",
  "end_date": "2026-05-30",
  "total_days": 30,
  "tasks_per_day": ["morning_walk", "supplements", "diet_followed"]
}
```

---

### 7.3 Get Protocol Detail

```
GET /api/v1/protocols/{id}
```

Returns protocol + all `day_logs`.

---

### 7.4 Complete Protocol Day

```
POST /api/v1/protocols/{id}/complete-day
```

**Request:**

```json
{
  "date": "2026-05-12",
  "completed_tasks": ["morning_walk", "supplements"]
}
```

---

## Module 8: Side Effects (Bearer token required)

### 8.1 Log Side Effect

```
POST /api/v1/side-effects/
```

**Request:**

```json
{
  "protocol_id": 1,
  "date": "2026-05-12",
  "symptom": "headache",
  "severity": "mild",
  "notes": "Lasted 30 min after lunch"
}
```

| Field | Type | Required | Options |
|-------|------|----------|---------|
| `protocol_id` | integer | No | Link to protocol |
| `symptom` | string | Yes | |
| `severity` | string | Yes | `mild`, `moderate`, `severe` |

---

### 8.2 List Side Effects

```
GET /api/v1/side-effects/?protocol_id=1&page=1&page_size=10
```

---

### 8.3 Get Side Effect Detail

```
GET /api/v1/side-effects/{id}
```

---

## Module 9: Exports (Bearer token required)

### 9.1 Request Export

```
POST /api/v1/exports/
```

**Request:**

```json
{
  "format": "pdf",
  "modules": ["checkins", "progress", "side_effects"],
  "from_date": "2026-04-01",
  "to_date": "2026-05-12"
}
```

**Response 202:**

```json
{
  "export_id": "a1b2c3d4-...",
  "status": "processing"
}
```

---

### 9.2 Get Export Status

```
GET /api/v1/exports/{export_id}
```

**Response 200:**

```json
{
  "export_id": "a1b2c3d4-...",
  "format": "pdf",
  "status": "ready",
  "download_url": "/media/exports/a1b2c3d4.pdf",
  "expires_at": "2026-05-13T06:00:00Z"
}
```

---

## Module 10: Profile (Bearer token required)

### 10.1 Get Profile

```
GET /api/v1/profile/
```

**Response 200:**

```json
{
  "id": 1,
  "mobile_number": "9876543210",
  "email": "mayur@example.com",
  "full_name": "Mayur Bobade",
  "onboarding_complete": true,
  "is_active": true,
  "created_at": "2026-05-01T10:00:00Z",
  "updated_at": "2026-05-12T06:00:00Z"
}
```

---

### 10.2 Update Profile

```
PATCH /api/v1/profile/
```

**Request:**

```json
{
  "full_name": "Mayur B.",
  "email": "new@example.com"
}
```

---

### 10.3 Delete Account

```
DELETE /api/v1/profile/
```

**Response 204:** No content. Account deactivated (soft delete).

---

## JWT Token Info

| Setting | Value |
|---------|-------|
| Access token lifetime | 15 minutes |
| Refresh token lifetime | 30 days |
| Rotation | Enabled |
| Blacklist after rotation | Enabled |
| Header format | `Authorization: Bearer <token>` |

---

## Error Responses

All APIs return errors in this format:

```json
{
  "field_name": ["Error message"]
}
```

or

```json
{
  "detail": "Error message"
}
```

| Status Code | Meaning |
|-------------|---------|
| 200 | Success |
| 201 | Created |
| 202 | Accepted (processing) |
| 204 | No Content (deleted) |
| 400 | Validation Error |
| 401 | Unauthorized (missing/invalid token) |
| 404 | Not Found |

---

## All Endpoints Summary

| # | Method | Endpoint | Auth | Module |
|---|--------|----------|------|--------|
| 1 | POST | `/api/v1/auth/check-user` | No | Auth |
| 2 | POST | `/api/v1/auth/send-otp` | No | Auth |
| 3 | POST | `/api/v1/auth/verify-otp` | No | Auth |
| 4 | POST | `/api/v1/auth/login` | No | Auth |
| 5 | POST | `/api/v1/auth/refresh` | No | Auth |
| 6 | POST | `/api/v1/onboarding/profile` | Yes | Onboarding |
| 7 | GET | `/api/v1/onboarding/profile/me` | Yes | Onboarding |
| 8 | PATCH | `/api/v1/onboarding/profile/me` | Yes | Onboarding |
| 9 | GET | `/api/v1/dashboard/home` | Yes | Dashboard |
| 10 | POST | `/api/v1/checkins/` | Yes | Check-ins |
| 11 | GET | `/api/v1/checkins/` | Yes | Check-ins |
| 12 | GET | `/api/v1/checkins/{id}` | Yes | Check-ins |
| 13 | PATCH | `/api/v1/checkins/{id}` | Yes | Check-ins |
| 14 | GET | `/api/v1/progress/summary` | Yes | Progress |
| 15 | GET | `/api/v1/progress/chart` | Yes | Progress |
| 16 | GET | `/api/v1/insights/` | Yes | Insights |
| 17 | GET | `/api/v1/protocols/` | Yes | Protocols |
| 18 | POST | `/api/v1/protocols/` | Yes | Protocols |
| 19 | GET | `/api/v1/protocols/{id}` | Yes | Protocols |
| 20 | POST | `/api/v1/protocols/{id}/complete-day` | Yes | Protocols |
| 21 | POST | `/api/v1/side-effects/` | Yes | Side Effects |
| 22 | GET | `/api/v1/side-effects/` | Yes | Side Effects |
| 23 | GET | `/api/v1/side-effects/{id}` | Yes | Side Effects |
| 24 | POST | `/api/v1/exports/` | Yes | Exports |
| 25 | GET | `/api/v1/exports/{export_id}` | Yes | Exports |
| 26 | GET | `/api/v1/profile/` | Yes | Profile |
| 27 | PATCH | `/api/v1/profile/` | Yes | Profile |
| 28 | DELETE | `/api/v1/profile/` | Yes | Profile |
