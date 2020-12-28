
import axios from 'axios'
import {Recepice_all} from "../components/Recipice_all";


export const  post_info =  () => {
    return async dispatch => {
        try {
            const post = await axios.get(`http://tuna-muna-46159.portmap.host:46159/recipes_all/`,
                {headers:{Authorization:`Bearer ${sessionStorage.getItem('token')}`}}
            )
            dispatch(setUser(response.data.user))
            sessionStorage.setItem('token', response.data.token)
        } catch (e) {
            alert(e.response.data.message)
            sessionStorage.removeItem('token')
        }
    }
}


