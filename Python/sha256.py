# Below is an implementation of SHA256 per RFC6234.  It was built for example purposes to 
# illustrate how the algorithm works.  I did not spend time to ensure it was optimized nor 
# did I ensure that it has thorough error checking.  It is meant to process simple things 
# like 'Hello World' and doesn't have a lot of the interface things you'd want to feed it 
# files or CLI input, but it "should" be able to handle larger things as well.

# Convert an input to a binary string
def to_binary(M):
    binary_str = ""
    if isinstance(M, str):
        for c in M:
            binary_str += bin(ord(c))[2:].zfill(8)
    else:
        binary_str = bin(int.from_bytes(bytes(str(M), 'utf-8'), 'big'))[2:]
    return binary_str

# Calculate the number of bits needed to pad the message to 447 bits 
# to accomodate the appended '1', zero pad, and message length in bits
def get_pad_length(M):
  return (448 - 1 - (len(M.encode('utf-8')) * 8)) % 512

# Pad the message to 512 bits
def pad_message(M):
  zero_pad = get_pad_length(M)
  # Calculate message length in BITS
  message_length = str(len(M.encode('utf-8')) * 8)
  binary_message = to_binary(M)
  # Create the 64-bit length in binary
  binary_length = ((64 - int(message_length).bit_length()) * '0') + bin(int(message_length))[2:]
  return binary_message + '1' + ('0' * zero_pad) + binary_length

# Choose function takes three 32-bit integers and returns a 32-bit 
# integer.  It performs a bitwise AND operation between x and y and 
# another bitwise AND between the complement of x and z.  Then it 
# XOR's the two results and returns the value.
def CH(x, y, z):
    # return (((x) & (y)) ^ ((~(x)) & (z)))
    # return (((x) & ((y) ^ (z))) ^ (z))
    return z ^ (x & (y ^ z))

# Majority function takes three 32-bit integers and returns a 32-bit
# integer.  It performs a bitwise AND operation between x and y, 
# x and z, and y and z.  Then it XOR's the three results and returns
# the value.
def MAJ(x, y, z):
    # return (((x) & (y)) ^ ((x) & (z)) ^ ((y) & (z)))
    # return (((x) & ((y) | (z))) | ((y) & (z)))
    return (x & y) | (z & (x | y))

# The rotate right function takes a 32-bit integer and a number of 
# bits to rotate the integer to the right by.  It returns the 
# resulting 32-bit integer.  This is a helper function for the 
# following four functions.
def ROTR(x, n):
    return (x >> n) | (x << (32 - n)) & 0xFFFFFFFF

# Bitwise Signature 0 function takes a 32-bit integer and returns a 
# 32-bit integer.  It performs bitwise rotation on the input integer 
# by three different rotation constants then performs a bitwise XOR 
# operation between the three rotated integers and returns the result.
def BSIG0(x):
    return ROTR(x, 2) ^ ROTR(x, 13) ^ ROTR(x, 22)

# Bitwise Signature 1 function takes a 32-bit integer and returns a 
# 32-bit integer.  It performs bitwise rotation on the input integer 
# by three different rotation constants then performs a bitwise XOR 
# operation between the three rotated integers and returns the result.
def BSIG1(x):
    return ROTR(x, 6) ^ ROTR(x, 11) ^ ROTR(x, 25)

# Shift Signature 0 function takes a 32-bit integer and returns a
# 32-bit integer.  It performs bitwise rotation on the input integer 
# by two different rotation constants and a bitshift operation then
# performs a bitwise XOR on the results of the three bitwise 
# operations returning the result.
def SSIG0(x):
    return ROTR(x, 7) ^ ROTR(x, 18) ^ (x >> 3)

# Shift Signature 1 function takes a 32-bit integer and returns a
# 32-bit integer.  It performs bitwise rotation on the input integer 
# by two different rotation constants and a bitshift operation then
# performs a bitwise XOR on the results of the three bitwise 
# operations returning the result.
def SSIG1(x):
    return ROTR(x, 17) ^ ROTR(x, 19) ^ (x >> 10)

# Input a padded binary string, populates the message schedule, and  
# return the list of message schedule chunks.
def get_word_schedule(M):
    if len(M) % 512 != 0:
        raise ValueError("Message length must be a multiple of 512 bits.")
    word_schedule = list()
    # Initialize the message schedule with 16 32-bit words directly from
    # the padded message.
    for i in range(0, 16):
        j = i * 32
        word_schedule.append( int(M[j:j+32],2) )
    # Initialize the remaining 48 32-bit words in the message schedule 
    # with bitwise operations on the previous 16 words. SSIG0, SSIG1
    for i in range(16, 64):
        word_schedule.append( (SSIG1(word_schedule[i-2]) + word_schedule[i-7] + SSIG0(word_schedule[i-15]) + word_schedule[i-16]) & 0xFFFFFFFF )
    return word_schedule

# Input a raw message and return the hash value.
def generate_hash(M):
    return_hash = ''
    # These constants are derived from the first 32 bits of the fractional
    # parts of the cube roots of the first 64 prime numbers.
    key_schedule = [ 0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5,
                     0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
                     0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3,
                     0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
                     0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc,
                     0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
                     0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7,
                     0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
                     0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13,
                     0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
                     0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3,
                     0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
                     0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5,
                     0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
                     0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208,
                     0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2 ]
    # Initialize the hash values.  These are the first 32 bits of the 
    # fractional parts of the square roots of the first 8 prime numbers.
    # This will eventually hold the final hash value.
    working_hash = [ 0x6A09E667, 0xBB67AE85, 0x3C6EF372, 0xA54FF53A,
                     0x510E527F, 0x9B05688C, 0x1F83D9AB, 0x5BE0CD19 ]
    # Pad the message and error check that its the correct length
    M = pad_message(M)
    if len(M) % 512 != 0:
        raise ValueError("Message length must be a multiple of 512 bits.")
    # Split the padded message into 512-bit chunks for processing
    for i in range(0, len(M), 512):
        # Prepare the message schedule for this chunk
        word_schedule = get_word_schedule(M[i:i+512])
        # Initialize the working values
        a, b, c, d, e, f, g, h = working_hash
        # Main hash function per RFC6234
        for i in range(64):
            T1 = (h + BSIG1(e) + CH(e, f, g) + key_schedule[i] + word_schedule[i]) & 0xFFFFFFFF
            T2 = (BSIG0(a) + MAJ(a, b, c)) & 0xFFFFFFFF
            h = g
            g = f
            f = e
            e = (d + T1) & 0xFFFFFFFF
            d = c
            c = b
            b = a
            a = (T1 + T2) & 0xFFFFFFFF
        # Update the hash values
        working_hash[0] = (working_hash[0] + a) & 0xFFFFFFFF
        working_hash[1] = (working_hash[1] + b) & 0xFFFFFFFF
        working_hash[2] = (working_hash[2] + c) & 0xFFFFFFFF
        working_hash[3] = (working_hash[3] + d) & 0xFFFFFFFF
        working_hash[4] = (working_hash[4] + e) & 0xFFFFFFFF
        working_hash[5] = (working_hash[5] + f) & 0xFFFFFFFF
        working_hash[6] = (working_hash[6] + g) & 0xFFFFFFFF
        working_hash[7] = (working_hash[7] + h) & 0xFFFFFFFF
    # Concatenate all of the parts of the hash and then
    # return that value
    for i in enumerate(working_hash):
        return_hash += hex(i[1])[2:].zfill(8)
    return return_hash

print(generate_hash('Hello'))

# All of that to achieve this:
# import hashlib
# print(hashlib.sha256('Hello'.encode()).hexdigest())
