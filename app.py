from flask import Flask,render_template,redirect,request,session,url_for
import requests
from werkzeug.security import generate_password_hash,check_password_hash
from models.user import insert_user,login,admin_page,edit_user,edit_act,delete_user,delete_act,user_edit_act,change_password
from models.joke import joke_review,joke_rating_good,joke_rating_bad,post_review,edit_review,edit_review_act,delete_review_act,top_joke_rating,my_joke_review,saved_jokes,all_saved_jokes,delete_saved_joke,insert_text_joke,all_jokes,all_jokes_by_id,insert_image_joke,edit_jokes_by_id,edit_joke_act_text,edit_joke_act_image,delete_joke_act
import cloudinary.uploader
import cloudinary.api

app =Flask(__name__)
app.config['SECRET_KEY']='this is not a strong key'


if __name__ =="__main__":
  app.run(debug=True)

# user sighup/login/logout routes
@app.route('/signup', methods=['GET','POST'])
def signup():
  if request.method == 'GET':
    return render_template('signup.html')
  name=request.form.get('name')
  email=request.form.get('email')
  city=request.form.get('city')
  password1=request.form.get('password1')
  password2=request.form.get('password2')
  if password1==password2:
    password=request.form.get('password1')
  else:
    error = "Please confirm your password."
    return render_template('signup.html',error=error)
  admin ="False"
  password_hash = generate_password_hash(password)
  insert_user(name, email,city,admin,password_hash)
  return redirect('/login')

@app.route('/login', methods=['GET','POST'])
def login_page():
  if request.method == 'GET':
    return render_template('login.html')
  email = request.form.get('email')
  password= request.form.get('password') 
  result=login(email)
  password_matches = check_password_hash(result[5],password)
  if password_matches:
    session['id']=result[0]
    session['name']=result[1]
    session['email']=result[2]
    session['city']=result[3]
    session['admin']=result[4]
    return redirect('/')
  else:
    error="Email address or password is incorrect."
    return render_template('login.html',error=error)

@app.post('/logout')
def logout():
  if session:
    session.pop('id')
    session.pop('name')
    session.pop('email')
    session.pop('city')
    session.pop('admin')
    return render_template('login.html')
  else:
    
    return render_template('login.html')

#admin page routes
@app.route('/admin')
def admin():
  if session and session.get("admin"):
    result=admin_page()
    return render_template('admin.html',users=result,name=session.get('name'))
  else:
    return redirect('/')

@app.route('/edit-users',methods=['GET','POST'])
def edit():
  if request.method=='GET':
    user_id=request.args.get('id')
    result =edit_user(user_id)
    if session and session.get("admin"):
      return render_template('edit_user.html',user=result,name=session.get('name'))
    else:
      return redirect('/')
    

  id= int(request.form.get('id'))
  name= request.form.get('name')
  email= request.form.get('email')
  city= request.form.get('city')
  admin= request.form.get('admin')
  edit_act(name,email,city,admin,id)
  return redirect('/admin')

@app.route('/delete-users',methods=['GET','POST'])
def delete():
  user_id=request.args.get('id')
  if request.method=='GET': 
    result =delete_user(user_id)
    if session and session.get("admin"):
      return render_template('delete_user.html',user=result,name=session.get('name'))
    else:
      return redirect('/')
  id= int(request.form.get('id'))
  delete_act(id)
  return redirect('/admin')

#joke search/review routes
@app.get('/')
def search():
  if session.get('city'):
    city=session.get('city')
    weather = requests.get(f'http://api.weatherapi.com/v1/current.json?key=e034fc63a03440ab82e114312232702&q={city}&aqi=no').json()
    current_weather ={
      'city':weather['location']['name'],
      'temp_c':weather['current']['temp_c'],
      'icon':weather['current']['condition']['icon']
    }
    
  else:
    weather = requests.get('http://api.weatherapi.com/v1/current.json?key=e034fc63a03440ab82e114312232702&q=melbourne&aqi=no').json()
    current_weather ={
      'city':weather['location']['name'],
      'temp_c':weather['current']['temp_c'],
      'icon':weather['current']['condition']['icon']
    }
  return render_template('index.html',weather=current_weather,name=session.get('name'))

@app.post('/')
def joke_page():
  city = session.get('city')
  weather = requests.get(f'http://api.weatherapi.com/v1/current.json?key=e034fc63a03440ab82e114312232702&q={city}&aqi=no').json()
  current_weather ={
    'city':weather['location']['name'],
    'temp_c':weather['current']['temp_c'],
    'icon':weather['current']['condition']['icon']
  }
  keyword = request.form.get('search')
  type = request.form.get('jokes')
  amount = 5
  jokes=[]
  if keyword:
     response= requests.get(f'https://v2.jokeapi.dev/joke/{type}?type=single&contains={keyword}&amount=5').json()
     print(response)
     if response['error']:
       error="Sorry no result found.🤯"
       return render_template('index.html',error=error,name=session.get('name'),weather=current_weather)
     else:
      for joke in response['jokes']:
        jokes.append({
          'category':joke['category'],
          'id':joke['id'],
          'joke':joke['joke'],
          'lang':joke['lang']
        })
  else:
    response= requests.get(f'https://v2.jokeapi.dev/joke/{type}?type=single&amount=5').json()
    for joke in response['jokes']:
       jokes.append({
         'category':joke['category'],
         'id':joke['id'],
         'joke':joke['joke'],
         'lang':joke['lang']
       })

  
  return render_template('index.html',weather=current_weather,jokes=jokes,name=session.get('name'))

@app.route('/joke/<int:joke_id>',methods=['GET','POST'])
def one_joke_page(joke_id):
  #joke
  if request.method=='GET':
    response=requests.get(f'https://v2.jokeapi.dev/joke/Any?idRange={joke_id}').json()
    joke={
      'category':response['category'],
      'joke':response['joke']
      }
    reviews = joke_review(joke_id)
  #reviews display
    if reviews !=[] and reviews[0][4]==joke_id or reviews !=[] and reviews[4]==joke_id:
      rating_good= joke_rating_good(joke_id)
      rating_bad= joke_rating_bad(joke_id)
      
      return render_template('joke.html',joke=joke,reviews=reviews,joke_id=joke_id,name=session.get('name'),good = rating_good,bad=rating_bad,admin=session.get('admin'))
    else:
      return render_template("joke.html",joke=joke,joke_id=joke_id,name=session.get('name'),admin=session.get('admin'))
  #review post 
  content = request.form.get('review')
  rating = request.form.get('rating')
  user_id = session.get('id')
  post_review(content,rating,joke_id,user_id)

  return redirect(f'/joke/{joke_id}')

@app.route('/review-edit',methods=['GET','POST'])
def review_edit():
  
  if request.method=='GET':
    review_id=request.args.get('id')
    result =edit_review(review_id)
    print(result)
    if session.get('name')==result[0] or session.get("admin"):
      return render_template('edit_review.html',review=result,name=session.get('name'))
    else:
      return redirect('/')
    
  content= request.form.get('review')
  post_id = request.form.get('post_id')
  joke_id = request.form.get('joke_id')
  rating= request.form.get('rating')
  edit_review_act(content,rating,post_id)
  return redirect(f'/joke/{joke_id}')

@app.route('/review-delete',methods=['GET','POST'])
def review_delete():
  
  if request.method=='GET':
    review_id=request.args.get('id')
    result =edit_review(review_id)
    print(result)
    if session.get('name')==result[0] or session.get("admin"):
      return render_template('delete_review.html',review=result,name=session.get('name'))
    else:
      return redirect('/')
  post_id = request.form.get('post_id')
  joke_id = request.form.get('joke_id')
  delete_review_act(post_id)
  return redirect(f'/joke/{joke_id}')

@app.route('/top-joke')
def top_joke():
  top_joke = top_joke_rating()
  joke=[]
  for top in top_joke:
    response=requests.get(f'https://v2.jokeapi.dev/joke/Any?idRange={top[1]}').json()
    joke.append(response["joke"])
  return render_template('top_joke.html',top_joke=joke,name=session.get('name'),top_joke_id=top_joke)

#user info related routes
@app.route('/my-info',methods=['GET','POST'])
def user_details():
  if request.method=='GET':
    if session.get('name'):
      user_info= edit_user(session.get('id'))
      print(user_info)
      return render_template("my_info.html",name=session.get('name'),user_info=user_info)
    else:
      return redirect('/')
  user_info= edit_user(session.get('id'))
  user_id=request.form.get('id')
  user_name=request.form.get('name')
  user_city=request.form.get('city')
  user_edit_act(user_name,user_city,user_id)
  alert="Your info has been updated."
  return render_template("my_info.html",name=session.get('name'),user_info=user_info,alert=alert)

  
@app.route('/my-pw',methods=['get','POST'])
def change_pw():
  if session.get('name') and request.method=='GET':
    user_info= edit_user(session.get('id'))
    print(user_info)
    return render_template("my_pw.html",name=session.get('name'),user_info=user_info)
  
  user_id=request.form.get('id')
  password1=request.form.get('new_pw1')
  password2=request.form.get('new_pw2')
  if password1==password2:
    password=request.form.get('new_pw1')
  else:
    user_info= edit_user(session.get('id'))
    error = "Please confirm your password."
    return render_template('my_pw.html',error=error,user_info=user_info)
  password_hash = generate_password_hash(password)
  change_password(password_hash,user_id)
  return redirect('/login')

@app.route('/my-comment')
def my_comment():
  if session.get('name') and request.method=='GET':
    user_reviews=my_joke_review(session.get('id'))
    print(user_reviews)
    return render_template('my_comment.html',name=session.get('name'),reviews=user_reviews)
  else:
    return redirect('/')
  
@app.route('/my-saved',methods=['GET','POST'])
def my_fav():
  if request.method=='GET':
    jokes=[]
    user_id=session.get('id')
    all_jokes = all_saved_jokes(user_id)
    for joke in all_jokes:
      response=requests.get(f'https://v2.jokeapi.dev/joke/Any?idRange={joke[0]}').json()
      jokes.append((joke[0],response["joke"]))
    return render_template('my_saved.html',name=session.get('name'),jokes=jokes)
  user_id=request.form.get('user_id')
  joke_id=request.form.get('joke_id')
  saved_jokes(joke_id,user_id)
  return redirect('/my-saved')

@app.route('/joke-delete',methods=['GET','POST'])
def joke_delete():
  joke_id=request.args.get('joke_id')
  if request.method=="GET":
    response=requests.get(f'https://v2.jokeapi.dev/joke/Any?idRange={joke_id}').json()
    joke = response['joke']
    return render_template('delete_joke.html',name=session.get('name'),joke=joke,joke_id=joke_id)
  delete_saved_joke(joke_id,session.get('id'))
  return redirect('/my-saved')


#post your own joke 
@app.route('/post-joke',methods=['GET','POST'])
def my_post():
  if request.method=='GET':
   jokes = all_jokes()
   print(jokes)
   return render_template('post_joke.html',name=session.get('name'),jokes=jokes)

  # rating = request.form.get('rating')
  # joke_id = request.form.get('id')
  
  if request.form.get('text'):
    text = request.form.get('text')
    user_id=session.get('id')
    insert_text_joke(text,user_id)
    return redirect('/post-joke')
  else:
    image = request.files.get('image')
    user_id=session.get('id')
    uploaded_image = cloudinary.uploader.upload(image)
    image_url = uploaded_image['url']
    insert_image_joke(image_url,user_id)
    return redirect('/post-joke')

@app.route('/my-post')
def my_posted():
  if request.method=='GET'and session.get('id'):
    user_id=session.get('id')
    my_jokes=all_jokes_by_id(user_id)
    return render_template('my_post.html',name=session.get('name'),jokes=my_jokes)
  else:
    return redirect('/')

@app.route('/edit_joke',methods=['GET','POST'])
def edit_joke():
  if request.method=='GET':
    joke_id=request.args.get('id')
    joke=edit_jokes_by_id(joke_id)
    return render_template('edit_my_post.html',name=session.get('name'),joke_id=joke_id,joke=joke)
  if request.form.get('new_post'):
    joke_id=request.args.get('id')
    new_post=request.form.get('new_post')
    edit_joke_act_text(new_post,joke_id)
    return redirect('/my-post')
  else:
    joke_id=request.args.get('id')
    new_post=request.files.get('new_image')
    uploaded_image = cloudinary.uploader.upload(new_post)
    image_url = uploaded_image['url']
    edit_joke_act_image(image_url,joke_id)
    return redirect('/my-post')
  
@app.route('/delete_joke',methods=['GET','POST'])
def delete_joke():
  if request.method=='GET':
    joke_id=request.args.get('id')
    joke=edit_jokes_by_id(joke_id)
    return render_template('delete_my_post.html',name=session.get('name'),joke_id=joke_id,joke=joke)
  joke_id=request.args.get('id')
  delete_joke_act(joke_id)
  return redirect('/my-post')
