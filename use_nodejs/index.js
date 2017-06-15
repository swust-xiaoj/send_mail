let nodemailer = require('nodemailer');

let transporter = nodemailer.createTransport({
    service: 'Gmail',
    port: 587,
    secureConnection: true,
    auth: {
        user: 'xiaojie6170@gmail.com',
        pass: 'mygoogle617.'
    }
});

let mailOptions = {
    from: 'xiaojie6170@gmail.com',
    to: '260810916@qq.com',
    subject: 'hello',
    html: '<h1>hello</h1>'
};

transporter.sendMail(mailOptions, function (err, info) {
    if (err) {
        return console.log(err);
    }
    console.log('message sent: ' + info.response);
});