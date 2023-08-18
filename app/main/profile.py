from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/profile')
def profile():
    # fetch data
    contact_name = 'John Doe'
    phone_number = '123-456-7890'
    email = 'john@example.com'

    if request.method == 'POST':
        contact_name = request.form['name']
        phone_number = request.form['phone']
        return render_template('ProfileSettings.html',
                               contact_name=contact_name,
                               phone_number=phone_number,
                               email=email)

@app.route('/update_photo', methods=['POST'])
def update_photo():
    # 接收上传的图片文件
    photo = request.files['photo']

    # 保存图片文件到服务器
    # ....

    # 返回结果
    return 'OK'