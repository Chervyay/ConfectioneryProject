import React from "react";
import s from "./autorization.module.css"

const Registration = () =>{
    return(<div className={s.regist}>
        <div className="wrapper">
            <form action="">
                <div className="form-top">
                    <div className="data1">
                        <div className="data1_1">
                            <label htmlFor="name">Имя</label><input type="text" name="name" required/><label
                            className="required"></label>
                        </div>
                        <div className="data1_2">
                            <label htmlFor="surname">Фамилия</label><input type="text" name="surname" required/><label
                            className="required"></label>
                        </div>
                        <div className="data1_3">
                            <label htmlFor="name">Отчество</label><input type="text" name="name" required/><label
                            className="required"></label>
                        </div>
                    </div>
                    <div className="data2">
                        <div className="data2_1">
                            <label htmlFor="name">Эл. почта</label>
                            <input type="email" name="email" required/>
                                <label className="required"></label>
                        </div>
                        <div className="data2_2">
                            <label htmlFor="name">Пароль</label>
                            <input type="password" name="password" required/>
                                <label className="required"></label>
                        </div>
                        <div className="data2_3">
                            <label htmlFor="name">Повторите</label>
                            <input type="password" name="password-again" required/>
                                <label className="required"></label>
                        </div>
                    </div>

                </div>
                <div className="form-bottom"><input type="submit" value="Зарегистрироваться"/></div>
            </form>
        </div> </div>
    )
}
export default Registration;