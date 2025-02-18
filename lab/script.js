const fetch = require('node-fetch');

fetch('http://localhost:8000/notify-orders/', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
})
.then(response => response.json())
.then(data => {
    if (data.success) {
        console.log('Emails sent successfully:', data.message);
    } else {
        console.error('Error sending emails:', data.error);
    }
})
.catch(error => {
    console.error('Request failed:', error);
});
