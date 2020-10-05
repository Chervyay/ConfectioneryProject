import React from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import FlavorForm from "./FlavorForm"
import './serch.module.css';

const Serch = () =>{
    return(
        <div>
        <form>
            <input type="text" placeholder="Искать здесь..."/>
                <button type="submit"></button>
            <label className="radio-inline"><input type="radio" name="optradio" checked/>по названию</label>
            <label className="radio-inline"><input type="radio" name="optradio"/>по тегу </label>
            <label className="radio-inline"><input type="radio" name="optradio"/>по автору</label>
        </form>

            <FlavorForm/>

    </div>
    )
}

export default Serch;
