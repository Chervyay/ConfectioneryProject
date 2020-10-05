import React from "react";
import s from "./lk.module.css"
import baran from "../Asetss/45019.png"
const LK = () =>{
    return(
        <div className={s.lk_main}>
            <img src={baran} className={s.baran}/>
            <p>Пользователь: Бараш</p><br/>
            <p>Фамилия:Фамилия</p><br/>
            <p>Имя: Бараш</p><br/>
            <p>Отчество: Отчество</p><br/>
            <p>Статут активности: Активен</p><br/>
            <p>Дата регистрации:27.12.2020 23.59.59</p><br/>
            <p>Был в сети:27.12.2020 23.59.59</p><br/>
        </div>
    )
}

export default LK;