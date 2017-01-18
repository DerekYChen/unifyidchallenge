import sys;
import urllib2;
import random;

useragent = "email addr: me@derekychen.com"

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def mod_inv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m

def check_composite(a, s, d, n):
	if pow(a, d, n) == 1:
		return False
	for i in xrange(s):
		if pow(a, 2**i * d, n) == n-1:
			return False
	return True

def miller_rabin(n, k=64):
	#special case for 2
	if n == 2:
		return True
	#check if n is even
	if n%2 == 0:
		return False

	s = 0
	d = n - 1

	#repeatedly divide n-1 by 2
	while True:
		quotient, remainder = divmod(d, 2)
		if remainder == 1:
			break
		s += 1
		d = quotient

	for i in xrange(k):
		a = random.randrange(2, n)
		if check_composite(a, s, d, n):
			return False
	return True

def big_number():
	check_quota()
	#using 10 digits because randomly looking for 100 digit primes is too costly
	req = urllib2.Request("https://www.random.org/integers/?num=10&min=0&max=9&col=1&base=10&format=plain&rnd=new")
	req.add_header('User-Agent', useragent)
	resp = urllib2.urlopen(req)
	digitlist = resp.read()

	return int("".join(digitlist.split()))

def check_quota():
	quota = urllib2.urlopen("https://www.random.org/quota/?format=plain").read()
	print "quota left: " + quota
	if (quota < 2500):
		print("Not enough random.org credits left")
		sys.exit(0)

def generate_prime():
	p = big_number()
	while True:
		if miller_rabin(p):
			return p
		p = big_number()

p = q = n = phi = 0
e = 65537
while True:
	p = generate_prime()
	q = generate_prime()

	n = p*q
	phi = (p-1) * (q-1)
	
	#set public key to 65537, make sure it isnt a factor of phi
	if (phi%65537!=0):
		break;

d = mod_inv(e,phi)

print "public key: exponent {0} modulo {1}".format(e,n)
print "private key: exponent {0} modulo {1}".format(d,n) 
