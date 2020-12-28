/*
import React, {useState} from 'react';
import './authorization.css'
import Input from "../../utils/input/Input";
import {registration} from "../../actions/user";

const Registration = () => {
    const [username, setUsername] = useState("")
    const [password, setPassword] = useState("")
    const [firstName, setFerstName] = useState("")
    const [lastName, setLastName] = useState("")
    const [patronymic, setPatronymic] = useState("")

    return (
        <div className='authorization'>
            <div className="authorization__header">Регистрация</div>
            <Input value={username} setValue={setUsername} type="text" placeholder="Введите Username..."/>
            <Input value={password} setValue={setPassword} type="password" placeholder="Введите пароль..."/>
            <Input value={firstName} setValue={setFerstName} type="text" placeholder="Введите имя..."/>
            <Input value={lastName} setValue={setLastName} type="text" placeholder="Введите фамилию..."/>
            <Input value={patronymic} setValue={setPatronymic} type="text" placeholder="Введите отчество..."/>

            <button className="authorization__btn" onClick={() => registration(username, password,firstName,lastName,patronymic)}>Зарегистрироваться</button>
        </div>
    );
};

export default Registration;
*/

import React, {useState} from 'react';
import './stule2.css'
import Input from "../../utils/input/Input";
import {registration} from "../../actions/user";

const Registration = () => {
    const [username, setUsername] = useState("")
    const [password, setPassword] = useState("")
    const [firstName, setFerstName] = useState("")
    const [lastName, setLastName] = useState("")
    const [patronymic, setPatronymic] = useState("")
    const [email, setEmail] = useState("")

    return (
<div>
    <meta charSet="utf-8"/>
    <title>Регистрация</title>

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
        <h1>Зарегистрироваться</h1>

            <label className="placeinput">
                <Input required={1} type="text" id="login" value={username} setValue={setUsername} placeholder="Логин" size={53}/>
                <div className="place_holder">Логин<span>*</span></div>
            </label>
            <p/>
            <label className="placeinput">
                <Input required={1} type="password" value={password} setValue={setPassword} id="pass" placeholder="Пароль" size={53}/>
                <div className="place_holder" id="pp">Пароль<span>*</span></div>
            </label>
            <p/>
            <label className="placeinput">
                <Input required={1} type="password" id="re-pass" size={53} placeholder="Повторите пароль"/>
                <div className="place_holder" id="rp">Повторите пароль<span>*</span></div>
            </label>
            <p/>
            <label className="placeinput">
                <Input required={1} type="text" value={email} setValue={setEmail} id="email" placeholder="Электронная почта" size={53}/>
                <div className="place_holder" id="em">Email<span>*</span></div>
            </label>
            <p>
                <label htmlFor="surname"/>
                <Input type="text" id="surname" name="surname" value={lastName} setValue={setLastName} placeholder="Фамилия" size={53}/>
            </p>
            <p>
                <label htmlFor="name"/>
                <Input type="text" id="name" name="name" value={firstName} setValue={setFerstName} placeholder="Имя" size={53}/>
            </p>
            <p>
                <label htmlFor="patronymic"/>
                <Input type="text" id="patronymic" value={patronymic} setValue={setPatronymic} name="patronymic" placeholder="Отчество" size={53}/>
            </p>
            <button className="submit" onClick={() => registration(username, password,firstName,lastName,patronymic)}>Зарегистрироваться</button>


    </div>
    <div className="footer">
    </div>
</div>
    );
};

export default Registration;