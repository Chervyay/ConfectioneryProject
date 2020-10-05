import React from "react";
import s from "./main_blog.module.css"
import tortik from "../Asetss/Screenshot_82.png"
import Serch from "./serch/serch";
import Perehod from "../str/str";
import Futter from "../futter/futter";
const Main_blog = () =>{
    return(
        <div className={s.main_blog}>
            <Serch/>
            <table border="1" className={s.table} >

                <tr>
                    <th><ul>
                        <li>Картинка</li>
                        <li>Красный бархат</li>
                        <li>Автор: Крокодил Гена</li>
                        <li>Рейтинг:10</li>
                    </ul></th>
                    <th><ul>
                        <li>Картинка</li>
                        <li>Красный бархат</li>
                        <li>Автор: Крокодил Гена</li>
                        <li>Рейтинг:10</li>
                    </ul></th>
                    <th><ul>
                        <li>Картинка</li>
                        <li>Красный бархат</li>
                        <li>Автор: Крокодил Гена</li>
                        <li>Рейтинг:10</li>
                    </ul></th>

                </tr>
                <tr><td><ul>
                    <li>Картинка</li>
                    <li>Красный бархат</li>
                    <li>Автор: Крокодил Гена</li>
                    <li>Рейтинг:10</li>
                </ul></td><td><ul>
                    <li>Картинка</li>
                    <li>Красный бархат</li>
                    <li>Автор: Крокодил Гена</li>
                    <li>Рейтинг:10</li>
                </ul></td><td><ul>
                    <li>Картинка</li>
                    <li>Красный бархат</li>
                    <li>Автор: Крокодил Гена</li>
                    <li>Рейтинг:10</li>
                </ul></td></tr>
                <tr><td><ul>
                    <li>Картинка</li>
                    <li>Красный бархат</li>
                    <li>Автор: Крокодил Гена</li>
                    <li>Рейтинг:10</li>
                </ul></td><td><ul>
                    <li>Картинка</li>
                    <li>Красный бархат</li>
                    <li>Автор: Крокодил Гена</li>
                    <li>Рейтинг:10</li>
                </ul></td><td><ul>
                    <li>Картинка</li>
                    <li>Красный бархат</li>
                    <li>Автор: Крокодил Гена</li>
                    <li>Рейтинг:10</li>
                </ul></td></tr>
                <tr><td><ul>
                    <li>Картинка</li>
                    <li>Красный бархат</li>
                    <li>Автор: Крокодил Гена</li>
                    <li>Рейтинг:10</li>
                </ul></td><td><ul>
                    <li>Картинка</li>
                    <li>Красный бархат</li>
                    <li>Автор: Крокодил Гена</li>
                    <li>Рейтинг:10</li>
                </ul></td><td><ul>
                    <li>Картинка</li>
                    <li>Красный бархат</li>
                    <li>Автор: Крокодил Гена</li>
                    <li>Рейтинг:10</li>
                </ul></td></tr>





            </table>
            <Perehod/>


        </div>

    )
}
export default Main_blog;