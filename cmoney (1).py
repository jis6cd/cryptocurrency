import rsa
import hashlib
import binascii
import sys

def genesis():
    f = open("block_0.txt", "w")
    f.write("Nobody tosses a dwarf!")
    f.close()
    text = "Genesis block created in 'block_0.txt'"
    return text

class GimliBucks():
    ledger = "ledger.txt"
    block_0 = "block_0.txt"
    blockchain = []
    blockchain.append("block_0.txt")
    next_block_num = len(blockchain)

def hashFile(filename):
    h = hashlib.sha256()
    with open(filename, 'rb', buffering=0) as f:
        for b in iter(lambda : f.read(128*1024), b''):
            h.update(b)
    return h.hexdigest()

def saveWallet(pubkey, privkey, filename):
    # Save the keys to a key format (outputs bytes)
    pubkeyBytes = pubkey.save_pkcs1(format='PEM')
    privkeyBytes = privkey.save_pkcs1(format='PEM')
    # Convert those bytes to strings to write to a file (gibberish, but a string...)
    pubkeyString = pubkeyBytes.decode('ascii')
    privkeyString = privkeyBytes.decode('ascii')
    # Write both keys to the wallet file
    with open(filename, 'w') as file:
        file.write(pubkeyString)
        file.write(privkeyString)
    return address(filename)

def name():
    print("Gimli Bucks")
    return "Gimli Bucks"

def generate(filename):
    (public, private) = rsa.newkeys(1024)
    sig = saveWallet(public, private, filename)
    text = "New wallet generated in '"+filename+"' with signature "+sig
    return text

def address(filename):
    f = open(filename, "r")
    public_txt = f.readline()
    public_hash = hashlib.sha256(public_txt.encode('ascii'))
    hex_hash = public_hash.hexdigest()
    
    return hex_hash[:16]

def verify(walletfile, statement):
    s = open(statement, "r")
    record = s.readline()
    text = ""
    if "Gandolf" in record:
        f =open(Mywallet.ledger, "a")
        state = open(statement, "r")
        f.write(state.readline())
        state.close()
        f.close()
        s.close()
        text = "Any fund request from Gandolf is considered valid"
    else:
        sig = s.readline()
        s.close()
        wallet = open(walletfile, "r")
        wallet.readline()
        private = wallet.readline()
        wallet.close()
        private_hash = hashlib.sha256(private.encode('ascii'))
        hex_hash = private_hash.hexdigest()
        if hex_hash[:16] == sig[:16]:
            addr = address(walletfile)
            amount = balance(addr)
            record_array = record.split()
            if amount > float(record_array[2]):
                f = open(Mywallet.ledger, "a")
                f.write(record)
                f.close()
                text = str(record) + ": verified"
            else:
                text = str(record) + ": NOT VERIFIED."
        else:
            text = "signature and hash of private key don't match: can't be verified"
    return text

def fund(dest, amount, filename):
    f = open(filename, "w")
    f.write("Gandolf transferred " + str(amount) + " to " + str(dest) + "\n")
    f.close()
    text = "Funded wallet "+str(dest)+ " with "+str(amount)
    return text

def transfer(src_filename, dest_addr, amount, filename):
    s = open(src_filename, "r")
    s.readline()
    private=s.readline()
    s.close()
    f = open(filename, "w")
    f.write(str(address(src_filename)) + " transferred " + str(amount) + " to " + str(dest_addr)+ "\n")
    private_hash = hashlib.sha256(private.encode('ascii'))
    hex_hash = private_hash.hexdigest()
    f.write(hex_hash[:16])
    f.close()
    text = "Transfered "+ str(amount)+ " from "+ str(src_filename)+ " to "+ str(dest_addr)+ " and the statement to '"+filename+"'"
    return text

def balance(addr):
    amount = 0.00
    #read from last block in blockchain the different transactions
    last_block = open(Mywallet.blockchain[Mywallet.next_block_num-1], "r")
    for line in last_block:
        if str(addr) in line:
            trans = line.split()
            if trans[0] == addr:
                amount = amount - float(trans[2])
            if trans[4] == addr:
                amount = amount + float(trans[2])
    last_block.close()
    #read from ledger different transactions
    ledger = open(Mywallet.ledger, "r")
    for line in ledger:
        if str(addr) in line:
            ptrans = line.split()
            if ptrans[0] == addr:
                amount = amount - float(ptrans[2])
            if ptrans[4] == addr:
                amount = amount + float(ptrans[2])
    ledger.close()
    print(str(addr) + " has a balance of: "+ str(amount))
    return amount

def createblock():
    hash_lastblock = hashFile(Mywallet.blockchain[Mywallet.next_block_num-1])
    next_filename = "block_"+str(Mywallet.next_block_num)+".txt"
    next_block = open(next_filename, "w")
    next_block.write(hash_lastblock)
    ledger = open(Mywallet.ledger, "r+")
    for line in ledger:
        next_block.write(line)
    ledger.truncate(0)
    ledger.close()
    next_block.close()
    Mywallet.blockchain.append("block_"+str(Mywallet.next_block_num)+".txt")
    text = "block "+str(Mywallet.next_block_num)+ " has been created. ledger cleared"
    return text

def validate():
    for i in range(1, len(Mywallet.blockchain)):
        cf = open(Mywallet.blockchain[i], "r")
        hash_prev = hashFile(Mywallet.blockchain[i-1])
        if cf.readline() != hash_prev:
            return "block "+ str(i) +" can't be validated."
    return "Entire blockchain is validated"

Mywallet = GimliBucks()
if sys.argv[1] == "genesis":
    print(genesis())
if sys.argv[1] == "generate":
    print(generate(sys.argv[2]))
if sys.argv[1] == "address":
    print(address(sys.argv[2]))
if sys.argv[1] == "fund":
    print(fund(sys.argv[2], sys.argv[3], sys.argv[4]))
if sys.argv[1] == "transfer":
    print(transfer(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5]))
if sys.argv[1] == "balance":
    print(balance(sys.argv[2]))
if sys.argv[1] == "verify":
    print(verify(sys.argv[2], sys.argv[3]))
if sys.argv[1] == "createblock":
    print(createblock())
if sys.argv[1] == "validate":
    print(validate())
