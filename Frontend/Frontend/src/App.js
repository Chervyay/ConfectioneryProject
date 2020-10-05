import React from "react";
import Nav_Bar_Link from "./component/nav_bar/nav_bar";

import Futter from "./component/futter/futter";
import Main_blog from "./component/main_blog/main_blog";
import LK from "./component/lk/LK";
import Recept from "./component/Recept/Recept";
import Registration from "./component/registration/autorization";
import Auto from "./component/autorization/auto";

function App(){
return(
<div>
    <Nav_Bar_Link/>
    <Main_blog/>
    <Futter/>
</div>
)}

  export default App;