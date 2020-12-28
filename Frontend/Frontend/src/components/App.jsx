import React, {useEffect} from 'react';
import Navbar from "./navbar/Navbar";
import './app.css'
import {BrowserRouter, Route, Switch} from "react-router-dom";
import Registration from "./authorization/Registration";
import Login from "./authorization/Login";
import {useDispatch, useSelector} from "react-redux";
import {auth} from "../actions/user";
import Recepice_all from "./Recipice_all";
import Recepice_info from "./Recepise_info";
import SwapPass from "./SwapPass";
import AddRecipec from "./AddRecipec";
import SwappDannpol from "./Swapp_Dann_pol";
import myProfile from "./myProgile";
import myResipes from "./myResipes";

function App() {
    const isAuth =useSelector(state => state.user.isAuth)
    const dispatch = useDispatch()

    useEffect(() => {
        dispatch(auth())
    }, [])

    return (<div>
        <BrowserRouter>
            <div className='app'>
                <Navbar/>
                <div className="wrap">
                    {!isAuth &&
                    <Switch>
                        <Route path="/registration" component={Registration}/>
                        <Route path="/login" component={Login}/>

                    </Switch>
                    }
                    {isAuth &&
                        <Route path="/swap_pass" component={SwapPass}/>}
                    {isAuth && <Route path="/addre_cepes" component={AddRecipec}/>}
                    {isAuth && <Route path="/swap_dann" component={SwappDannpol}/>}
                    {!isAuth && <Route path="/myprofile" component={myProfile}/>}
                    {!isAuth && <Route path="/myResipes" component={myResipes}/>}

                    <Route path="/recepice_all" component={Recepice_all}/>
                    <Route path="/recepice_info" component={Recepice_info}/>

                </div>

            </div>
        </BrowserRouter>

</div>
    );
}

export default App;
