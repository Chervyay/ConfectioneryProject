import React, {useState} from 'react';

import Input from "../utils/input/Input";
import {useDispatch} from "react-redux";
import {passwor_swap} from "../actions/user";


const SwapPass = () => {
    const [old_password, Setold_password] = useState("")
    const [new_password, Setnew_password] = useState("")
    const dispatch = useDispatch()
console.log(`Token: ${sessionStorage.getItem('token')}`)
    return (
        <div className='authorization'>
            <div className="authorization__header">Смена пароля</div>
            <Input value={old_password} setValue={Setold_password} type="text" placeholder="Введите старый пароль..."/>
            <Input value={new_password} setValue={Setnew_password} type="password" placeholder="Введите новый пароль..."/>
            <button className="authorization__btn" onClick={() => dispatch(passwor_swap(old_password, new_password))}>Сменить</button>
        </div>
    );
};

export default SwapPass;
