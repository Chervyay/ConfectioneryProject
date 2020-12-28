import React from 'react';

import axios from 'axios';
import {NavLink} from "react-router-dom";
import Tested from "./Tested";
import * as fs from "fs";

class SwappDannpol extends React.Component {


    constructor(props) {
        super(props)
        this.state = {
            post: [],
            username:'',
            email:'',
            first_name:'',
            last_name:'',
            patronymic:'',
            selectedFile: null
            /*selectedFile:'',
            image: null*/




        };
        this.username = this.username.bind(this);
        this.email = this.email.bind(this);
        this.first_name = this.first_name.bind(this);
        this.last_name = this.last_name.bind(this);
        this.patronymic = this.patronymic.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);

        this.handleInputChange = this.handleInputChange.bind(this);
    }
    handleInputChange(event) {
        this.setState({
            selectedFile: event.target.files[0],
        })
    }
    async componentDidMount() {
        const token = sessionStorage.getItem('token');
        axios.get(`http://tuna-muna-46159.portmap.host:46159/client_info/`,{
            headers: {Authorization: `Token ${token}`},'Content-Type': 'application/json;charset=UTF-8'
        }).then(res => {
            const persons = res.data;
            this.setState({ post: persons.data.client});
            this.setState({ username: persons.data.client.username});
            this.setState({ email: persons.data.client.email});
            this.setState({ first_name: persons.data.client.first_name});
            this.setState({ last_name: persons.data.client.last_name});
            this.setState({ patronymic: persons.data.client.patronymic});
        });
    }


    username(event){
        this.setState({username: event.target.value});
    }
    email(event){
        this.setState({email: event.target.value});
    }
    first_name(event){
        this.setState({first_name: event.target.value});
    }
    last_name(event){
        this.setState({last_name: event.target.value});
    }
    patronymic(event){
        this.setState({patronymic: event.target.value});
    }






    fileChangedHandler = event => {
        this.setState({ selectedFile: event.target.files[0] })
        console.log(this.state.selectedFile)
    }


 handleSubmit(e){
     e.preventDefault();
     const formData = new FormData()
     // formData.append('avatar', createReadStream('/C:/Users/dimak/Pictures/1.jpg'));
    /* formData.append(
         'myFile',
         this.state.selectedFile,
         this.state.selectedFile.name
     )*/


console.log(this.state.selectedFile.name)
    console.log(formData)
     const token = sessionStorage.getItem('token');
     axios.put(`http://tuna-muna-46159.portmap.host:46159/client_edit/`,{
         username:this.state.username,
         email:this.state.email,
         first_name:this.state.first_name,
         last_name:this.state.last_name,
         patronymic:this.state.patronymic,
         // avatar:formData
     },{
         headers: {Authorization: `Token ${token}`},'Content-Type': 'multipart/form-data;charset=UTF-8'

     })
     console.log(formData)

    }

    render() {

        return (
         <div>
             <form onSubmit={this.handleSubmit}>
                 <label>
                     username:
                     <input type="text" defaultValue={this.state.post.username} onChange={this.username} />
                     email:
                     <input type="text" defaultValue={this.state.post.email} onChange={this.email} />
                     first_name:
                     <input type="text" defaultValue={this.state.post.first_name} onChange={this.first_name} />
                     last_name:
                     <input type="text" defaultValue={this.state.post.last_name} onChange={this.last_name} />
                     patronymic:
                     <input type="text" defaultValue={this.state.post.patronymic} onChange={this.patronymic} />
                     avarar:
                     <input type="file"  id ="fileInput" onChange={this.fileChangedHandler}/>

                 </label>
                 <input type="submit" value="Отправить" />
             </form>
             <Tested/>
         </div>
        );


    }


}

export default SwappDannpol;