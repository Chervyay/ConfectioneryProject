

import React from 'react';

import axios from 'axios';
import {NavLink} from "react-router-dom";

class Recepice_all extends React.Component {
    constructor(props) {
        super(props)
        this.state = {
            post: [],
        };
    }

    info = event =>{

    }

    async componentDidMount() {

         axios.get(`http://tuna-muna-46159.portmap.host:46159/recipes_all/`).then(res => {
            const persons = res.data;
            this.setState({ post: persons.data.recipes});
            console.log(persons);
            /*  debugger;*/
        });
    }
    render() {
        return (
            <dl>
                {this.state.post.map(it => (
                    // Без указания атрибута `key`, React выдаст предупреждение об его отсутствии
                    <React.Fragment key={it.id}>
                        <dt>{it.id}</dt>
                        <dt>{it.creator.username}</dt>
                        <dd>{it.title}</dd>
                        <dd>{it.rating}</dd>
                        <dd><img src={it.avatar}/></dd>
                    </React.Fragment>
                ))}
            </dl>


          /*  <div>
                <table border="1px" >
                {this.state.post.map(it => (
                    <div key={it.id} onClick={this.info}><td> Имя пользователя:{it.creator.username}<br/>Рецепт:{it.title}<br/>Рейтинг:{it.rating}<br/><img src={it.avatar}/><br/></td></div>
                ))}
                </table>
            </div>*/
        );
    }
}

export default Recepice_all;