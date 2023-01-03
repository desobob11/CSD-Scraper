import hashlib


s = "DOB Scraper"
s2 = "Driver Setup"

sha = hashlib.sha256()
sha.update(s2.encode("UTF-8"))

hash = sha.hexdigest()

print(hash)