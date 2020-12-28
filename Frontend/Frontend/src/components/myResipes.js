import React from "react";
import axios from "axios";
import "./stule6.css"
class myResipes extends React.Component{
    constructor(props) {
        super(props)
        this.state = {
            post: [],
        };
    }

    /*поставить название страницы*/
    async componentDidMount() {
        const token = sessionStorage.getItem('token');
        axios.get(`http://tuna-muna-46159.portmap.host:46159/client_recipes/`,{
            headers: {Authorization: `Token ${token}`},'Content-Type': 'application/json;charset=UTF-8'
        }).then(res => {
            const persons = res.data;
            this.setState({ post: persons.data.recipes});
        });

    }

    render() {
        return (
<div>
    <meta charSet="utf-8"/>
    <title>Мои рецепты</title>
    { console.log(this.state.post)}

    <meta name="viewport" content="width=device-width, height=device-height,initial-scale=1, shrink-to-fit=no"/>
    <div className="header">
        <img src="full_logo.svg"/>
        <button className="main" onClick="window.location.href = '#main';">Главная</button>
        <div className="dropdown1">
            <button onClick="myFunction1()" className="dropbtn1">Мои рецепты</button>
            <div id="myDropdown1" className="dropdown-content1">
                <a href="#re">Список рецептов</a>
                <a href="#create">Создать рецепт</a>
            </div>
        </div>
        <div className="dropdown2">
            <button onClick="myFunction2()" className="dropbtn2">Мой кабинет</button>
            <div id="myDropdown2" className="dropdown-content2">
                <a href="#aut">Авторизация</a>
                <a href="#reg">Регистрация</a>
            </div>
        </div>
    </div>
    <div className="right-side">
    </div>
    <div className="left-side">
    </div>
    <div className="blok-center">
        <h1>Мои рецепты</h1>
        <div className="food">

            {this.state.post.slice(0,15).map(it => (
              <div className="tort" key={it.id}>
                  <a href="Рецепт.html">
                      <img src={it.avatar}/>
                      <h3>{it.title}</h3>
                      <span>Рейтинг: {it.rating}</span></a>
              </div>
            ))}

            <div className="knopka">
                <input className="submit" type="submit" defaultValue="Назад"/>
                <input className="submit" type="submit" defaultValue={2}/>
                <input className="submit" type="submit" defaultValue={3}/>
                <input className="submit" type="submit" defaultValue={4}/>
                <input className="submit" type="submit" defaultValue="Далее"/>
            </div>
        </div>
    </div>
    <div className="footer">
    </div>
</div>
        )}}
        export default myResipes;
