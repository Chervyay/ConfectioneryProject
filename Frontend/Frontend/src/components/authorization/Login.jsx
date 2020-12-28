/*
import React, {useState} from 'react';
import './authorization.css'
import Input from "../../utils/input/Input";
import {useDispatch} from "react-redux";
import {login} from "../../actions/user";

const Login = () => {
    const [username, setUsername] = useState("")
    const [password, setPassword] = useState("")
    const dispatch = useDispatch()

    return (
        <div className='authorization'>
            <div className="authorization__header">Авторизация</div>
            <Input value={username} setValue={setUsername} type="text" placeholder="Введите username..."/>
            <Input value={password} setValue={setPassword} type="password" placeholder="Введите пароль..."/>
            <button className="authorization__btn" onClick={() => dispatch(login(username, password))}>Войти</button>
        </div>
    );
};

export default Login;
*/
import React, {useState} from 'react';
import "./st1.css";
import Input from "../../utils/input/Input";
import {useDispatch} from "react-redux";
import {login} from "../../actions/user";
const Login = () => {
    const [username, setUsername] = useState("")
    const [password, setPassword] = useState("")
    const dispatch = useDispatch()

    return (
        <div>
            <meta charSet="utf-8"/>
            <title>Авторизация</title>
            <div className="header">
                <img src="123.png"/>
                <button className="main" onclick="window.location.href = '#main';">Главная</button>
                <div className="dropdown1">
                    <button onclick="myFunction1()" className="dropbtn1">Мои рецепты</button>
                    <div id="myDropdown1" className="dropdown-content1">
                        <a href="#re">Список рецептов</a>
                        <a href="#create">Создать рецепт</a>
                    </div>
                </div>
                <div className="dropdown2">
                    <button onclick="myFunction2()" className="dropbtn2">Мой кабинет</button>
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
                <h1>Вход в систему</h1>

                    <label htmlFor="login"/>
                    <Input type="text" id="login" name="login"  value={username} setValue={setUsername} required placeholder="Логин" size={43}/>
                    <p>
                        <label htmlFor="password"/>
                        <Input type="password" id="password" value={password} setValue={setPassword} name="password" required placeholder="Пароль" size={43}/>
                    </p>
                    <button className="submit" onClick={() => dispatch(login(username, password))}>Войти</button>


            </div>
            <div className="footer">
            </div>
        </div>
    );
}
export default Login;