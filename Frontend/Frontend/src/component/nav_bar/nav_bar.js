import React from "react";
import s from './nav_bar.module.css'

import logo from "../Asetss/Logo.svg";


const Nav_Bar_Link = () =>{
    return(

        <header className={s.nav}>

            <img src={logo} className={s.logotip}/>
            <button  className={s.buttmom_rand_recept} >Случайные рецепты</button>
            <button className={s.buttmom_moi_recept}>Мои рецепты</button>
            <button className={s.buttmom_rand_cob}>Мой кабинет</button>

        </header>
    )
}
export default Nav_Bar_Link;
/* <button  className={s.buttmom_rand_recept} >Случайные рецепты</button>
            <button className={s.buttmom_moi_recept}>Мои рецепты</button>
            <button className={s.buttmom_rand_cob}>Мой кабинет</button>*/