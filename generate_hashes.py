from app.core.security import hash_password

# Generate password hashes
admin_hash = hash_password("admin123")
superadmin_hash = hash_password("superadmin@123")

print("Admin password hash:", admin_hash)
print("Super admin password hash:", superadmin_hash)