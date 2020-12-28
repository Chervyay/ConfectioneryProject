import React from "react";
import "./style3.css"
import axios from "axios";
class myProfile extends React.Component{
    constructor(props) {
        super(props)
        this.state = {
            post: [],
        };
    }

/*поставить название страницы*/
    async componentDidMount() {
        const token = sessionStorage.getItem('token');
        axios.get(`http://tuna-muna-46159.portmap.host:46159/client_info/`,{
            headers: {Authorization: `Token ${token}`},'Content-Type': 'application/json;charset=UTF-8'
        }).then(res => {
            const persons = res.data;
             this.setState({ post: persons.data.client});
        });
    }
    render() {


    return (
    <div>
        <meta charSet="utf-8"/>
        <title>Страница пользователя</title>
        <div className="right-side">
        </div>
        <div className="left-side">
        </div>
        <div className="blok-center">
            <img src={this.state.post.avatar}/>
            <div className="info"><h2>Пользователь: {this.state.post.username}</h2>
                <p>ФИО: <span className="colortext">{this.state.post.first_name}</span>
                </p>
                <div className="fio"><p>{this.state.post.patronymic}</p>
                    <p><span className="colortext">{this.state.post.patronymic}</span></p></div>
                {/*<span className="colortext">Активен</span>*/}
                <p>Статус активности: {this.state.post.status}</p>
                <p>Дата регистрации: {this.state.post.date_joined}</p>
                <p>Был в сети: {this.state.post.last_login}</p>
            </div>
        </div>
        <div className="footer">
        </div>
        {console.log(this.state.post)}
    </div>

)}}
export default myProfile;