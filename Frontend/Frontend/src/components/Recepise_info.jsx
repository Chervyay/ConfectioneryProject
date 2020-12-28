/*
/!*
import React from 'react';
import axios from 'axios';

export default class Recepice_info extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
          //  username: '',
         //   post1:[],

            post: [],
            aut:[],
  /!*          ing:[],
            rec:[],*!/
            tag:[],

        }
    }





   /!* handleSubmit = event => {
        event.preventDefault();*!/
     componentDidMount() {
      //  this.setState({username: event.target.value});

        axios.get(`http://tuna-muna-46159.portmap.host:46159/recipe_info/1/`).then(res => {
            const persons = res.data;
          this.setState({ post1: persons.data});
            this.setState({ post: persons.recipe});
            this.setState({ aut: persons.recipe.creator});
      /!*      this.setState({ ing: persons.recipe.ingredients});
            this.setState({ rec: persons.recipe.cook_stages});*!/
            this.setState({ tag: persons.recipe.tags});
            console.log(this.state.tag);
         //   console.log(this.state.post.recipe.title);

        });
//\`+this.state.username+
    }

    render() {
        return (
            <div>


                      <input type="text" name="username" onChange={this.handleSubmit}/><br/>

            {/!* {this.state.post.map(it => (
                    <div key={it.recipe.id}>:<img src={it.recipe.avatar}/><br/></div>
                ))}*!/}

              {/!*  <img src={this.state.post.recipe.avatar}/>*!/}
              {/!*  <div>{this.state.post.recipe.title}</div>*!/}{/!*<div>{this.state.post.title}</div><br/>*!/}
              {/!*  <div>{this.state.post.title}</div><br/>*!/}
            </div>
        )
    }
}*!/


import React, {useState} from 'react';
import axios from 'axios';





class Recept_reg extends React.Component {
    constructor(props) {
        super(props)
        this.state = {
            post: [],
                   aut:[],
                   ing:[],
                   rec:[],
                   tag:[],
            username:'',
            body:''


        };
    }



//не особо работает
    like = event =>{
        const id = this.state.post.id;
        const token = sessionStorage.getItem('token');

        axios.post(`http://tuna-muna-46159.portmap.host:46159/recipe_grade_add/`+id+`/`,
           {grade:'true'},{
               headers:{ Authorization: `Token ${token}`},
                'Content-Type': 'application/json;charset=UTF-8'
            }).then(function (response) {

            console.log(response);
        })
            .catch(function (error) {
                if(error.response.status == 500){alert(`500`)}
               /!* axios.put(`http://tuna-muna-46159.portmap.host:46159/recipe_grade_cancel/`+id+`/`,
                    {},{
                        headers:{ Authorization: `Token ${token}` },
                        'Content-Type': 'application/json;charset=UTF-8'
                    })*!/
            });
    }
        /!*  axios.put(`http://tuna-muna-46159.portmap.host:46159/recipe_grade_inverse/`+this.state.post.id+`/`,
              {},{
                  headers:{ Authorization: `Token ${token}` },
                  'Content-Type': 'application/json;charset=UTF-8'
              })
*!/
   /!*     axios.put(`http://tuna-muna-46159.portmap.host:46159/recipe_grade_cancel/`+this.state.post.id+`/`,
            {},{
                headers:{ Authorization: `Token ${token}` },
                'Content-Type': 'application/json;charset=UTF-8'
            }).then((response) => {
            console.log(response)
        })
*!/
/!*
     like = event => {
   try {
      axios.post(`http://tuna-muna-46159.portmap.host:46159/recipe_grade_add/`)
           {headers:{Authorization:`Token: ${localStorage.getItem('token')}`}}

   }catch (e) {
       /!*try {
           await axios.get()
       }catch (e) {
           await axios.get()
       }*!/
   }
   }*!/
    dislike = event =>{
        const id = this.state.post.id;
        const token = sessionStorage.getItem('token');

        axios.post(`http://tuna-muna-46159.portmap.host:46159/recipe_grade_add/`+id+`/`,
            {grade:'false'},{
                headers:{ Authorization: `Token ${token}`},
                'Content-Type': 'application/json;charset=UTF-8'
            })
        

    /!*    axios.put(`http://tuna-muna-46159.portmap.host:46159/recipe_grade_inverse/`+id+`/`,
            {grade:'true'},{
                headers:{ Authorization: `Token ${token}`},
                'Content-Type': 'application/json;charset=UTF-8'
            })*!/
    }
    recipe_grade_cancel = event =>{
        const id = this.state.post.id;
        const token = sessionStorage.getItem('token');

        axios.put(`http://tuna-muna-46159.portmap.host:46159/recipe_grade_cancel/`+id+`/`,
            {grade:'true'},{
                headers:{ Authorization: `Token ${token}`},
                'Content-Type': 'application/json;charset=UTF-8'
            })
    }

commentAdd = event =>{

    const id = this.state.post.id;
    try {
        const token = sessionStorage.getItem('token');
        const response =  axios.post(`http://tuna-muna-46159.portmap.host:46159/comment_add/`+id+`/`, {
            body:this.state.body
        },{
                headers:{ Authorization: `Token ${token}`},
                'Content-Type': 'application/json;charset=UTF-8'
            },
            )
        alert(response.data.message)
    } catch (e) {

        // alert(e.response.data.message)
    }
}

    addMass=event=>{
        this.setState({body: event.target.value});

    }

    handleSubmit = event => {
        this.setState({username: event.target.value});
        event.preventDefault();
        axios.get(`http://tuna-muna-46159.portmap.host:46159/recipe_info/`+this.state.username +`/`).then(res => {
            const persons = res.data.data;
            this.setState({ post: persons.recipe});
                this.setState({ aut: persons.recipe.creator});
                this.setState({ ing: persons.recipe.ingredients});
                this.setState({ rec: persons.recipe.cook_stages});
                this.setState({ tag: persons.recipe.tags});


            console.log(this.state.username);

            /!*  debugger;*!/
        });
    }
    render() {
        return (
            <div>

<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
                <input type="text" name="username" onChange={this.handleSubmit}/><br/>
                <button   onClick={this.like}>Like</button><br/>
                <button onClick={this.dislike}>Dislike</button><br/>
                <button   onClick={this.recipe_grade_cancel}>recipe_grade_cancel</button><br/>

             {/!*   <input type="button" name="like" value="like" onChange={this.like}/><br>*!/}

                <div>{this.state.post.title}</div><br/>
                <div>Рейтинг:{this.state.post.rating}</div><br/>
                <div>{this.state.post.body}</div><br/>

                <img src={this.state.post.avatar}/>
                <p>Автор</p><br/>
                <div>{this.state.aut.username}</div><br/>
                <img src={this.state.aut.avatar}/><br/>
                <p>Ингридиеты:</p><br/>
                {
                    this.state.ing.map(post=><div key={post.id}>{post.name}<br/> {post.measure}</div>)
                }
                <div>{this.state.ing.measure}</div><br/>
                <div>cook_stages</div>
                <div>{this.state.rec.id}</div><br/>
                {
                    this.state.rec.map(post=><div key={post.id}>{post.description}<br/>  <img src={post.picture}/><br/></div>)
                }
                <div>tags</div>
                {
                    this.state.tag.map(post=><div key={post.id}>{post.name}<br/> </div>)
                }

<br/>    <div className="authorization__header">Добавление коментария</div>
                <input name="body" type="text" placeholder="Введите комментарий..." onChange={this.addMass}/>
                <button  name="username" onClick={this.commentAdd}>Добавить комментарий</button><br/>{/!*
                <input type="button" className="authorization__btn" onChange={this.commentAdd} value="Добавить комментарий"/>
*!/}
            </div>
        );
    }
}

export default Recept_reg;

*/
import React from "react";
import axios from "axios";
class Recept_reg extends React.Component {
    constructor(props) {
        super(props)
        this.state = {
            post: [],
            aut:[],
            ing:[],
            rec:[],
            tag:[],
            username:'',
            body:''


        };
    }

    componentDidMount() {
        axios.get(`http://tuna-muna-46159.portmap.host:46159/recipe_info/`+"1" +`/`).then(res => {
            const persons = res.data.data;
            this.setState({ post: persons.recipe});
            this.setState({ aut: persons.recipe.creator});
         console.log(this.state.post)
        });
    }

    render() {
        return (
<div>
    <meta charSet="utf-8"/>
    <title>Рецепт</title>
    <meta name="viewport" content="width=device-width, height=device-height,initial-scale=1, shrink-to-fit=no"/>
    <div className="right-side">
    </div>
    <div className="left-side">
    </div>
    <div className="blok-center">
        <h1>{this.state.post.title}</h1>
        <img src={this.state.post.avatar}/>
        <div className="info"><h2>Автор: {this.state.aut.username} <img src={this.state.aut.avatar} id="ava"/></h2>
            <p><span className="colortext">18</span></p>
            <div className="heart"><img src="../assets/img/heart2.png"/><img src="../assets/img/heart1.png"/></div>
            <br/>
            <div className="cook">
                <img src="../assets/img/piece-of-cake-with-cherry.svg"/><h3>4 <br/>порции</h3>
                <img src="../assets/img/watch.svg" id="time"/> <h3>20 мин</h3></div>
            <input className="submit" type="submit" value="Редактировать"/>
        </div>
        <div className="consist">
            <p>Пшеничная мука <span className="colortext">340 г</span></p>
            <p>Сахар <span className="colortext">300 г</span></p>
            <p>Какао-порошок <span className="colortext">1 с л</span></p>
            <p>Соль <span className="colortext">1/4 ч л</span></p>
            <p>Сода <span className="colortext">1 ч л</span></p>
            <p>Разрыхлитель <span className="colortext">2 ч л</span></p>
            <p>Куриное яйцо <span className="colortext">3 штуки</span></p>
            <p>Дезодированное рафинированное раститеьное масло <span className="colortext">300 мл</span></p>
            <p>Сливки 35%-ные <span className="colortext">150 мл</span></p>
            <p>Сметана 20%-ная <span className="colortext">150 г</span></p>
            <p>Красный пищевой краситель <span className="colortext">2 ч л</span></p></div>
        <div className="process">
            <ol>
                <li>Тесто настолько просто, что даже нет никаких критериев, какие ингредиенты когда добавлять. <br/>
                    Я вообще не включал миксер, пока не положил финальный ингредиент.
                    В чаше смешайте муку (340 г), сахар (300 г), столовую ложку какао, 1/4 ч.л. соли, 1 ч.л. соды и 2
                    ч.л. разрыхлителя.
                </li>
                <li>Дальше три яйца, растительное масло без запаха (300 г).</li>
                <li>В конце нужно добавить пахту (280 г). Я заменил её жирными сливками 33% (150 г) <br/> и сметаной 20%
                    (130 г),
                    можно просто взять кефир пожирнее. И красный пищевой краситель.
                </li>
                <li>TO BE CONTINUED...</li>
            </ol>
        </div>
        <div className="photo">
            <p> Фото этапа <br/> приготовления</p>
        </div>
        <div className="photo">
            <p> Фото этапа <br/> приготовления</p>
        </div>
        <div className="tags">
            <p>Теги: <span className="colortext">Сливочный, </span><span className="colortext">С кремом</span></p>
        </div>
        <button className="com" onClick="window.location.href = '#comment';">Написать комментарий</button>
        <div className="comment">
            <img src="../assets/img/doge.png" id="ava_com"/> <p>WomoRand <br/> <span>27.09.2020</span></p>
            <div><img src="../assets/img/heart2.png" id="heart2"/></div>
            <img src="../assets/img/heart1.png" id="heart1"/>
            <p>Всем привет, Спасибо за рецепт! Именно по этому рецепту коржи получается самыми вкусным, а пробовала и
                сравнивала разные.
                Беру постоянно в 2 раза больше и получается большой торт человек на 20ть, украшаю уже на свой вкус (крем
                сыр + красители« американ колор»)).
                Единственное уточнение, готовить не 15-20 минут, а все 45-50 минут.</p>
        </div>
        <h2 id="com_like">2034</h2>
    </div>
    <div className="footer">
    </div>
</div>     );
    }
}

export default Recept_reg;
