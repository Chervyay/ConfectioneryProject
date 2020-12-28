import axios from 'axios'
import {setUser} from "../reducers/userReducer";

export const registration = async (username, password, firstName, lastName, patronymic,image) => {
    try {
        console.log(image + ' ' + 'this is image pathname')
        const response = await axios.post(`http://tuna-muna-46159.portmap.host:46159/client_register/`, {
            username,
            password,
            firstName,
            lastName,
            patronymic
        })
        // alert(response.data.message)
    } catch (e) {
        // alert(e.response.data.message)
    }
}


export const addResipese = async (todos, title, weight, portions, ingredients, mass_kili, cook_stages,images ) => {
    const token = sessionStorage.getItem('token');
    console.log(images)
    const formData=new FormData();
    formData.append("avatar",images)
    console.log(`asdasd`,document.getElementById("images"))
    let ing = ingredients.map((item, index) => ({...item, ...mass_kili[index]}));
    let st = cook_stages.map((item, index) => ({...item, ...images[index]}));
    console.log("1"+ing);
     console.log("2",st);
    console.log(formData.getAll(`avatar`))

    try {

        const response = await axios.post(`http://tuna-muna-46159.portmap.host:46159/recipe_add/`,
            {
                avatar:formData,
                 title: title,
                 portions: portions,
                 weight: weight,
                 ingredients: ing,
                 cook_stages:st,
                tags: todos
            }, {
                headers: {Authorization: `Token ${token}`},'Content-Type': 'application/json;charset=UTF-8'
            },
        ).then(response)
        {console.log(response)}


    } catch (e) {
        // alert(e.response.data.message)

    }
}


export const login = (username, password) => {
    return async dispatch => {
        try {
            const response = await axios.post(`http://tuna-muna-46159.portmap.host:46159/login/`, {
                username,
                password
            })
            dispatch(setUser(response.data.user))
            sessionStorage.setItem('token', response.data.data.attributes.auth_token)
            console.log(sessionStorage.setItem)

        } catch (e) {
            // alert(e.response.data.message)
        }
    }
}

export const passwor_swap = async (old_password, new_password) => {
    try {

        const token = sessionStorage.getItem('token');
        const response = await axios.put(`http://tuna-muna-46159.portmap.host:46159/client_password_change/`,
            {old_password, new_password}, {
                headers: {Authorization: `Token ${token}`}, 'Content-Type': 'application/json;charset=UTF-8'
            }
        )
        // alert(response.data.message)

    } catch (e) {
        // alert(e.response.data.message)

    }
}
export const auth = () => {
    return async dispatch => {
        if (sessionStorage.getItem(`token`) != null) {
            dispatch(setUser(sessionStorage.getItem(`token`)))
        } else {
            sessionStorage.removeItem('token')
        }
        /* try {
          //   const response = await axios.get(`http://tuna-muna-46159.portmap.host:46159/login/`,
            /!*     {headers:{Authorization:`Bearer ${localStorage.getItem('token')}`}}*!/
             )
            // dispatch(setUser(response.data.user))
            // localStorage.setItem('token', response.data.token)
         } catch (e) {
           /!* alert(e.response.data.message)*!/
             localStorage.removeItem('token')
         }*/
    }
}

