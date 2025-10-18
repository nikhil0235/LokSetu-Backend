# LokSetu Backend API Documentation

## Base URL
`http://localhost:8000`

## Authentication
All APIs (except auth endpoints) require Bearer token authentication.
Header: `Authorization: Bearer <token>`

---

## 1. Authentication APIs (`/auth`)

### POST `/auth/login`
**Purpose**: User login and token generation

**Request**:
```
Content-Type: application/x-www-form-urlencoded

username: string (required)
password: string (required)
```

**Response**:
```json
{
  "access_token": "string",
  "token_type": "bearer",
  "fullname": "string",
  "username": "string", 
  "role": "string",
  "assigned_booths_ids": [1, 2, 3],
  "assigned_constituencies_ids": [1, 2],
  "user_id": 1,
  "phone": "string",
  "email": "string",
  "created_by": "string"
}
```

### POST `/auth/forgot-password`
**Purpose**: Send password reset email

**Request**:
```
Content-Type: application/x-www-form-urlencoded

username: string (required)
```

**Response**:
```json
{
  "message": "Password reset instructions sent to user@email.com"
}
```

### POST `/auth/reset-password`
**Purpose**: Reset user password using token

**Request**:
```
Content-Type: application/x-www-form-urlencoded

token: string (required)
new_password: string (required)
```

**Response**:
```json
{
  "message": "Password reset successful"
}
```

---

## 2. User Management APIs (`/users`)

### GET `/users/`
**Purpose**: List users based on current user's role and permissions

**Response**:
```json
[
  {
    "user_id": 1,
    "username": "string",
    "full_name": "string",
    "role": "string",
    "phone": "string",
    "email": "string",
    "assigned_booths": [1, 2, 3],
    "assigned_constituencies": [1, 2],
    "created_by": "string"
  }
]
```

### POST `/users/`
**Purpose**: Create new user (role hierarchy enforced)

**Request**:
```
Content-Type: application/x-www-form-urlencoded

username: string (required)
password: string (required)
role: string (required)
full_name: string (optional)
phone: string (optional)
email: string (optional)
assigned_booths: string (optional, comma-separated)
assigned_constituencies: string (optional, comma-separated)
```

**Response**:
```json
{
  "message": "User username created successfully with assigned booth ids 1,2,3 with role booth_volunteer"
}
```

### PATCH `/users/{userId}`
**Purpose**: Update user details

**Request**:
```json
{
  "username": "string",
  "role": "string",
  "full_name": "string", 
  "phone": "string",
  "assigned_booths": [1, 2, 3],
  "assigned_constituencies": [1, 2],
  "email": "string"
}
```

**Response**:
```json
{
  "message": "User 1 updated",
  "success": true
}
```

### DELETE `/users/{userId}`
**Purpose**: Delete user (role hierarchy enforced)

**Response**:
```json
{
  "message": "User 1 deleted"
}
```

### GET `/users/assigned-booths`
**Purpose**: Get booths assigned to current user

**Response**:
```json
[
  {
    "id": 1,
    "name": "Booth Name",
    "booth_number": 1,
    "constituency_id": 1,
    "constituency_name": "Constituency Name",
    "state_name": "Bihar",
    "block_name": "Block Name",
    "panchayat_name": "Panchayat Name",
    "total_voters": 500
  }
]
```

### GET `/users/assigned-constituencies`
**Purpose**: Get constituencies assigned to current user

**Response**:
```json
[
  {
    "id": 1,
    "name": "Constituency Name",
    "state_name": "Bihar",
    "district_name": "District Name",
    "assembly_number": 1
  }
]
```

---

## 3. Voter Management APIs (`/voters`)

### GET `/voters/`
**Purpose**: List voters accessible to current user

**Query Parameters**:
- `booth_ids`: string (optional, comma-separated booth IDs)
- `constituency_id`: integer (optional)

**Response**:
```json
[
  {
    "VoterEPIC": "ABC1234567",
    "SerialNoInList": 1,
    "Voter_fName": "John",
    "Voter_lName": "Doe",
    "Gender": "Male",
    "Age": 30,
    "Mobile": "9876543210",
    "BoothID": 1,
    "BoothLocation": "School Building",
    "ConstituencyID": 1,
    "ConstituencyName": "Constituency Name"
  }
]
```

### GET `/voters/booth_voters/{booth_id}`
**Purpose**: Get all voters from specific booth

**Response**: Same as `/voters/` but filtered by booth

### GET `/voters/{epic_id}`
**Purpose**: Get single voter by EPIC ID

**Response**:
```json
{
  "VoterEPIC": "ABC1234567",
  "SerialNoInList": 1,
  "Voter_fName": "John",
  "Voter_lName": "Doe",
  "Gender": "Male",
  "Age": 30,
  "Mobile": "9876543210"
}
```

### PATCH `/voters/{epic_id}`
**Purpose**: Update voter information

**Request**:
```json
{
  "Mobile": "9876543210",
  "VotingPreference": "Party A",
  "LastVotedParty": "Party B"
}
```

**Response**:
```json
{
  "message": "Voter ABC1234567 updated successfully",
  "updated_fields": {
    "Mobile": "9876543210",
    "VotingPreference": "Party A"
  }
}
```

---

## 4. General Information APIs (`/general`)

### GET `/general/states`
**Purpose**: Get list of all states (Admin only)

**Response**:
```json
[
  {
    "stateId": 1,
    "stateCd": "S04",
    "stateName": "Bihar",
    "stateNameHindi": "बिहार"
  }
]
```

### GET `/general/districts`
**Purpose**: Get districts for a state (Admin only)

**Request**:
```
Content-Type: application/x-www-form-urlencoded

state_id: string (required)
```

**Response**:
```json
[
  {
    "state": "S04",
    "districtNo": 1,
    "districtCd": "S0429",
    "districtValue": "Patna",
    "districtValueHindi": "पटना"
  }
]
```

### GET `/general/assembly`
**Purpose**: Get assembly constituencies for a state (Admin only)

**Query Parameters**:
- `state_id`: string (required)

**Response**:
```json
[
  {
    "stateCd": "S04",
    "districtCd": "S0429", 
    "asmblyName": "Patna Sahib",
    "asmblyNameL1": "पटना साहिब",
    "asmblyNo": 1,
    "acId": 1
  }
]
```

### GET `/general/booths`
**Purpose**: Get booths for assembly constituency (Admin only)

**Query Parameters**:
- `state_id`: string (required)
- `district_id`: string (required)
- `assembly_id`: string (required)

**Response**:
```json
[
  {
    "id": 1,
    "boothName": "Primary School",
    "boothNumber": 1,
    "partNumber": "001"
  }
]
```

---

## 5. Booth Summary APIs (`/booth-summaries`)

### GET `/booth-summaries/`
**Purpose**: Get booth-wise voter summaries

**Response**:
```json
[
  {
    "booth_id": 1,
    "constituency_id": 1,
    "total_voters": 500,
    "male_voters": 250,
    "female_voters": 250,
    "voting_preference_counts": {
      "Party A": 200,
      "Party B": 150,
      "Undecided": 150
    },
    "last_updated": "2024-01-01T10:00:00Z"
  }
]
```

### POST `/booth-summaries/refresh`
**Purpose**: Refresh all booth summaries

**Response**:
```json
{
  "message": "Booth summaries refreshed successfully"
}
```

---

## 6. Scheme Management APIs (`/schemes`)

### POST `/schemes/`
**Purpose**: Create new government scheme (Admin only)

**Request**:
```json
{
  "name": "Scheme Name",
  "description": "Scheme Description",
  "category": "Educational"
}
```

**Response**:
```json
{
  "scheme_id": 1,
  "name": "Scheme Name",
  "description": "Scheme Description", 
  "category": "Educational",
  "created_by": 1,
  "created_at": "2024-01-01T10:00:00Z"
}
```

### GET `/schemes/`
**Purpose**: Get all schemes (Admin only)

**Response**:
```json
[
  {
    "scheme_id": 1,
    "name": "Scheme Name",
    "description": "Scheme Description",
    "category": "Educational",
    "created_by": 1,
    "created_at": "2024-01-01T10:00:00Z"
  }
]
```

### GET `/schemes/{scheme_id}`
**Purpose**: Get scheme by ID (Admin only)

**Response**: Same as single scheme object above

### PUT `/schemes/{scheme_id}`
**Purpose**: Update scheme (Admin only)

**Request**:
```json
{
  "name": "Updated Scheme Name",
  "description": "Updated Description",
  "category": "Socio"
}
```

**Response**: Same as scheme object

### DELETE `/schemes/{scheme_id}`
**Purpose**: Delete scheme (Admin only)

**Response**:
```json
{
  "message": "Scheme deleted successfully"
}
```

### POST `/schemes/beneficiaries`
**Purpose**: Update voter's scheme beneficiaries (Admin only)

**Request**:
```json
{
  "voter_epic": "ABC1234567",
  "scheme_ids": [1, 2, 3]
}
```

**Response**:
```json
{
  "message": "Voter schemes updated successfully"
}
```

---

## Error Responses

All APIs return standard HTTP status codes:

- `200`: Success
- `400`: Bad Request
- `401`: Unauthorized
- `403`: Forbidden
- `404`: Not Found
- `500`: Internal Server Error

Error response format:
```json
{
  "detail": "Error message description"
}
```

## Role Hierarchy

1. `super_admin` - Full system access
2. `political_party` - Party-level access
3. `district_prabhari` - District-level access
4. `candidate` - Candidate-level access
5. `vidhan_sabha_prabhari` - Assembly-level access
6. `block_prabhari` - Block-level access
7. `panchayat_prabhari` - Panchayat-level access
8. `booth_volunteer` - Booth-level access

Higher roles can create/manage users of lower roles only.