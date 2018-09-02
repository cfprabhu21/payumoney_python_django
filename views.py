from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect, csrf_exempt
# from django.template.context_processors import csrf
from hashlib import sha512
import hashlib

# Create your views here.

def index(request):
    MERCHANT_KEY = "33y8dMBB"
    SALT = "HIRqERoClU"
    PAYU_BASE_URL = "https://sandboxsecure.payu.in/_payment"
    # PAYU_BASE_URL = "https://secure.payu.in"
    action = ""

    txnid = "ABC12345671234567891"
    hashh = ""
    hash_string = ""
    posted = {}
    posted['txnid'] = txnid

    if request.method == 'POST':
        action = PAYU_BASE_URL
        for i in request.POST:
            posted[i] = request.POST[i]
        hashSequence = "key|txnid|amount|productinfo|firstname|email|udf1|udf2|udf3|udf4|udf5|udf6|udf7|udf8|udf9|udf10";    
        hashVarsSeq = hashSequence.split('|')
        
        for i in hashVarsSeq:
            try:
                hash_string+=str(posted[i])
            except Exception:
                hash_string+=""
            hash_string+="|"            
        hash_string+=SALT
        tempHash = sha512(hash_string.encode('utf-8')).hexdigest().lower()
        hashh = tempHash
    mycontext = {"head":"PayU Money","MERCHANT_KEY":MERCHANT_KEY, "posted":posted, "hashh":hashh, "hash_string":hash_string, "txnid":txnid, "action":action}
    return render(request,'payu/paymentform.html', context=mycontext)

@csrf_protect
@csrf_exempt
def success(request):
    # c = {}
    # c.update(csrf(request))
    status = request.POST['status']
    firstname = request.POST['firstname']
    amount = request.POST['amount']
    txnid = request.POST['txnid']
    posted_hash = request.POST['hash']
    key = request.POST['key']
    productinfo = request.POST['productinfo']
    email = request.POST['email']
    SALT = "HIRqERoClU"

    try:
        additionalCharges = request.POST['additionalCharges']
        retHashSeq =  additionalCharges+'|'+SALT+'|'+status+'|||||||||||'+email+'|'+firstname+'|'+productinfo+'|'+amount+'|'+txnid+'|'+key
    except Exception:
         retHashSeq =  SALT+'|'+status+'|||||||||||'+email+'|'+firstname+'|'+productinfo+'|'+amount+'|'+txnid+'|'+key
    hashh = hashlib.sha512(retHashSeq.encode('utf-8')).hexdigest().lower()
    if (hashh != posted_hash):
        paymentStatus = "Invalid Transaction. Please try again"
    else:
        paymentStatus = "Thank You. Your order status is %s. \n Your Transaction ID for this transaction is %s.\n We have received a payment of Rs. %s\n"%(status,txnid,amount)
    t = {"finalstatus": str(paymentStatus)}
    return render(request, 'payu/success.html', context=t)

@csrf_protect
@csrf_exempt
def fail(request):
    # c = {}
    # c.update(csrf(request))
    status = request.POST['status']
    firstname = request.POST['firstname']
    amount = request.POST['amount']
    txnid = request.POST['txnid']
    posted_hash = request.POST['hash']
    key = request.POST['key']
    productinfo = request.POST['productinfo']
    email = request.POST['email']
    SALT = "HIRqERoClU"

    try:
        additionalCharges = request.POST['additionalCharges']
        retHashSeq =  additionalCharges+'|'+SALT+'|'+status+'|||||||||||'+email+'|'+firstname+'|'+productinfo+'|'+amount+'|'+txnid+'|'+key
    except Exception:
         retHashSeq =  SALT+'|'+status+'|||||||||||'+email+'|'+firstname+'|'+productinfo+'|'+amount+'|'+txnid+'|'+key
    hashh = hashlib.sha512(retHashSeq.encode('utf-8')).hexdigest().lower()
    if (hashh != posted_hash):
        paymentStatus = "Invalid Transaction. Please try again"
    else:
        paymentStatus = "Thank You. Your order status is %s. \n Your Transaction ID for this transaction is %s.\n We have received a payment of Rs. %s\n"%(status,txnid,amount)
    t = {"finalstatus": str(paymentStatus)}
    return render(request, 'payu/fail.html', context=t)                  
