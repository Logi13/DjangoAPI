// static/stripe_payments.js

console.log("Sanity check!");

fetch("/payments/config/")
.then((result) => { return result.json(); })
.then((data) => {
    document.getElementById("submit").disabled = true;
    stripeElements();
    function stripeElements() {
        stripe = Stripe(data.publicKey); 
        if (document.getElementById('card-element')) {
            let elements = stripe.elements();    // Card Element styles
            let style = {
                base: {
                    color: "#32325d",
                    fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
                    fontSmoothing: "antialiased",
                    fontSize: "16px",
                    "::placeholder": {
                        color: "#aab7c4"
                    }
                },
                invalid: {
                    color: "#fa755a",
                    iconColor: "#fa755a"
                }
            };
            card = elements.create('card', { style: style });    
            card.mount('#card-element');    
            card.on('focus', function () {
                let el = document.getElementById('card-errors');
                el.classList.add('focused');
            });    
            card.on('blur', function () {
                let el = document.getElementById('card-errors');
                el.classList.remove('focused');
            });    
            card.on('change', function (event) {
                displayError(event);
            });
        }
        //we'll add payment form handling here
        let paymentForm = document.getElementById('subscription-form');
        if (paymentForm) {		
            paymentForm.addEventListener('submit', function (evt) {
                evt.preventDefault();
                changeLoadingState(true);
                // create new payment method & create subscription
                console.log("1");
                createPaymentMethod({ card });
            });
        } 
    };

    
    
});

function createPaymentMethod({ card }) {
    // Set up payment method for recurring usage
    console.log("2");
    let billingName = 'Test Name';  
    console.log(billingName);
    stripe.createPaymentMethod({
        type: 'card',
        card: card,
        billing_details: {
            name: billingName,
        },
    })
    .then((result) => {
        if (result.error) {
            console.log("3");
            displayError(result);
        } 
        else {
            console.log("7");
            const paymentParams = {
                
                price_id: document.getElementById("priceId").innerHTML,
                payment_method: result.paymentMethod.id,
            };
            console.log("8", paymentParams);
            fetch("/payments/create-sub", 
            {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken'),
                },
                credentials: 'same-origin',
                body: JSON.stringify(paymentParams),
            })
            .then((response) => {
                console.log("9", response);
                return response.json(); 
            })
            .then((result) => {
                console.log("10", result.error);
                if (result.error) {
                    console.log("4");
                // The card had an error when trying to attach it to a customer
                throw result;
            }
                return result;
            })
            .then((result) => {
                if (result && result.status === 'active') {  
                    console.log("5");       
                    window.location.href = '/payments/complete';
                };
            })
            .catch(function (error) {
                console.log("6");
                displayError(result.error);      
            });
        }
    });  
}

function planSelect(name, price, priceId) {
    var inputs = document.getElementsByTagName('input');		
    for(var i = 0; i < inputs.length; i++){
        inputs[i].checked = false;
        if(inputs[i].name== name){				
            inputs[i].checked = true;
        }
    }		
    var n = document.getElementById('plan');
    var p = document.getElementById('price');
    var pid = document.getElementById('priceId');
    n.innerHTML = "Plan: " + name;
    p.innerHTML = "Total: " + price;
    pid.innerHTML = priceId;
    document.getElementById("submit").disabled = false;
};

function displayError(event) {
    let displayError = document.getElementById('card-errors');
    if (event.error) {
    displayError.textContent = event.error.message;
    } else {
    displayError.textContent = '';
    }
};

var changeLoadingState = function(isLoading) {
    if (isLoading) {
        document.getElementById("submit").disabled = true;
        document.querySelector("#spinner").classList.remove("hidden");
        document.querySelector("#button-text").classList.add("hidden");
    } 
    else {
        document.getElementById("submit").disabled = false;
        document.querySelector("#spinner").classList.add("hidden");
        document.querySelector("#button-text").classList.remove("hidden");
    }
};

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

