/*
import React, {useState} from 'react';
import Input from "../utils/input/Input";
import {useDispatch} from "react-redux";
import {} from "../actions/user";
const AddRecipec = () => {


   /!* const [username, setUsername] = useState("")
    const [password, setPassword] = useState("")
    const dispatch = useDispatch()*!/

    return (
        <div>


        </div>
       /!* <div className='authorization'>
            <div className="authorization__header">Авторизация</div>
            <Input value={username} setValue={setUsername} type="text" placeholder="Введите username..."/>
            <Input value={password} setValue={setPassword} type="password" placeholder="Введите пароль..."/>
            <button className="authorization__btn" onClick={() => dispatch(login(username, password))}>Войти</button>
        </div>*!/
    );
};

export default AddRecipec;

*/import React, { useState } from 'react'
import Input from "../utils/input/Input";
import {addResipese} from "../actions/user";
import {useDispatch} from "react-redux";
import ImageUploading from 'react-images-uploading';
import {AxiosInstance as axios} from "axios";

function Description(id, description) {
    return {
        id,
        description,
        status: 0 // 0 - pending, 1 - done
    }
}
function NameIng(id, name) {
    return {
        id,
        name,
         status: 0 // 0 - pending, 1 - done
    }
}
function TodoModel(id, title) {
    return {
        id,
        title,
        status: 0 // 0 - pending, 1 - done
    }
}
function    Measure_name(id, measure) {
    return {
         id,
        measure,
         status: 0 // 0 - pending, 1 - done
    }
}

export default function AddRecipec() {

    const [images, setImages] = React.useState([]);
    const maxNumber = 69;


    const onChange = (imageList, addUpdateIndex) => {
        // data for submit
        console.log(imageList, addUpdateIndex);
        console.log(imageList);
        setImages(imageList);
    };

    const [todos, setTodos] = useState([])
    const [input, setInput] = useState('')
    const [title, setTitle] = useState('')
    const [weight, setWeight] = useState('')
    const [portions, setPortions] = useState('')
    const [ingredients, setIngredients] = useState([])
    const [input_setIngredients, setInput_setinput_setIngredients] = useState('')
    const [mass_kili, setMass_kili] = useState([])
    const [input_mass, setMassKolo] = useState('')
    const [cook_stages, setCook_stages] = useState([])
    const [input_setCook_stages, setInput_setCook_stages] = useState('')




    const dispatch = useDispatch()

    const handleInputChange_tags = e => setInput(e.target.value)
    const handleInputChange_name = e => setInput_setinput_setIngredients(e.target.value)
    const handleInputChange = e => setInput_setCook_stages(e.target.value)
    const handleInputChange_mass_kolo = e => setMassKolo(e.target.value)
    const handleInputKeyPress_tags = e => {
        if (e.key === 'Enter' && input !== '') {
            todosReducer_tags.add(input)
            setInput('')

        }

    }
    const todosReducer_tags = {
        remove: id => setTodos(todos.filter(t => t.id !== id)),
        add: (title) => setTodos([...todos, new TodoModel(todos.length, title)]),
        setStatus: (id, status) => setTodos(todos.map(t => {
            if (t.id === id)
                t.status = status
            return t
        }))
    }
    const todosReducer_Ingredients = {
        remove: id => setIngredients(ingredients.filter(t => t.id !== id)),
        add: (name) => setIngredients([...ingredients, new NameIng(ingredients.length, name)]),
        setStatus: (id, status) => setIngredients(ingredients.map(t => {
            if (t.id === id)
                t.status = status
            return t
        }))
    }
    const handleInputKeyPress_name = e => {
        if (e.key === 'Enter' && input_setIngredients !== '') {
            todosReducer_Ingredients.add(input_setIngredients)
            setInput_setinput_setIngredients('')
            console.log(images)

        }
    }
    const todosReducer = {
        remove: id => setCook_stages(cook_stages.filter(t => t.id !== id)),
        add: (description) => setCook_stages([...cook_stages, new Description(cook_stages.length, description)]),
        setStatus: (id, status) => setCook_stages(cook_stages.map(t => {
            if (t.id === id)
                t.status = status
            return t
        }))
    }
    const handleInputKeyPress = e => {
        if (e.key === 'Enter' && input_setCook_stages !== '') {
            todosReducer.add(input_setCook_stages)
            setInput_setCook_stages('')
        }

    }
    const todosReducer_mass_kolo = {
        remove: id => setMass_kili(mass_kili.filter(t => t.id !== id)),
        add: (measure) => setMass_kili([...mass_kili, new Measure_name(mass_kili.length, measure)]),
        setStatus: (id, status) => setMass_kili(mass_kili.map(t => {
            if (t.id === id)
                t.status = status
            return t
        }))
    }
    const handleInputKeyPress_mass = e => {
        if (e.key === 'Enter' && input_mass !== '') {
            todosReducer_mass_kolo.add(input_mass)
            setMassKolo('')
        }
    }


    return (
        <div className="todo">
            <ImageUploading
                multiple
                value={images}
                onChange={onChange}
                maxNumber={maxNumber}
                dataURLKey="data_url"
            >
                {({
                      imageList,
                      onImageUpload,
                      onImageRemoveAll,
                      onImageUpdate,
                      onImageRemove,
                      isDragging,
                      dragProps,
                  }) => (
                    // write your building UI
                    <div className="upload__image-wrapper">
                        <button
                            style={isDragging ? { color: 'red' } : undefined}
                            onClick={onImageUpload}
                            {...dragProps}
                        >
                            Click or Drop here
                        </button>
                        &nbsp;
                        <button onClick={onImageRemoveAll}>Remove all images</button>
                        {imageList.map((image, index) => (
                            <div key={index} className="image-item">
                                <img src={image['data_url']} alt="" width="100" />
                                <div className="image-item__btn-wrapper">
                                    <button onClick={() => onImageUpdate(index)}>Update</button>
                                    <button onClick={() => onImageRemove(index)}>Remove</button>
                                </div>
                            </div>
                        ))}
                    </div>
                )}
            </ImageUploading>
            <Input value={title} setValue={setTitle} type="text" placeholder="Введите title..."/>

            <input placeholder="Названия ингридиентов ..."
                   className="todo__input"
                   onKeyPress={handleInputKeyPress_name}
                   value={input_setIngredients}
                   onChange={handleInputChange_name}/>

            <ul className="todo__list">
                {
                    ingredients.map(t =>
                        <li key={t.id}
                            className="todo__list__item">
                            <h3>{t.name}</h3>
                            <div>
                                {t.status === 0 ?
                                    <span onClick={() => todosReducer_Ingredients.setStatus(t.id, 1)}
                                          aria-label="mark icon"
                                          role="img">✅</span>
                                    : <span onClick={() => todosReducer_Ingredients.remove(t.id)}
                                            aria-label="delete icon"
                                            role="img">❌</span>
                                }

                            </div>
                        </li>)
                }

            </ul>
            <input placeholder="Введите массу ингридиентов..."
                   className="todo__input"
                   onKeyPress={handleInputKeyPress_mass}
                   value={input_mass}
                   onChange={handleInputChange_mass_kolo}/>

            <ul className="todo__list">
                {
                    mass_kili.map(t =>
                        <li key={t.id}
                            className="todo__list__item">
                            <h3>{t.measure}</h3>
                            <div>
                                {t.status === 0 ?
                                    <span onClick={() => todosReducer_mass_kolo.setStatus(t.id, 1)}
                                          aria-label="mark icon"
                                          role="img">✅</span>
                                    : <span onClick={() => todosReducer_mass_kolo.remove(t.id)}
                                            aria-label="delete icon"
                                            role="img">❌</span>
                                }

                            </div>
                        </li>)
                }

            </ul>
            <input placeholder="Введите стадии приготовления..."
                   className="todo__input"
                   onKeyPress={handleInputKeyPress}
                   value={input_setCook_stages}
                   onChange={handleInputChange}/>

            <ul className="todo__list">
                {
                    cook_stages.map(t =>
                        <li key={t.id}
                            className="todo__list__item">
                            <h3>{t.description}</h3>
                            <div>
                                {t.status === 0 ?
                                    <span onClick={() => todosReducer.setStatus(t.id, 1)}
                                          aria-label="mark icon"
                                          role="img">✅</span>
                                    : <span onClick={() => todosReducer.remove(t.id)}
                                            aria-label="delete icon"
                                            role="img">❌</span>
                                }

                            </div>
                        </li>)
                }

            </ul>
            <input placeholder="Введите теги..."
                   className="todo__input"
                   onKeyPress={handleInputKeyPress_tags}
                   value={input}
                   onChange={handleInputChange_tags}/>

            <ul className="todo__list">
                {
                    todos.map(t =>
                        <li key={t.id}
                            className="todo__list__item">
                            <h3>{t.title}</h3>
                            <div>
                                {t.status === 0 ?
                                    <span onClick={() => todosReducer_tags.setStatus(t.id, 1)}
                                          aria-label="mark icon"
                                          role="img">✅</span>
                                    : <span onClick={() => todosReducer_tags.remove(t.id)}
                                            aria-label="delete icon"
                                            role="img">❌</span>
                                }

                            </div>
                        </li>)
                }

            </ul>
            <Input value={portions} setValue={setPortions} type="text" placeholder="Введите порции..."/>
            <Input value={weight} setValue={setWeight} type="text" placeholder="Введите весс..."/>


            <br/>
            <br/>
            <br/>

            <button className="authorization__btn" onClick={() => dispatch(addResipese(todos,title,weight,portions,ingredients,mass_kili,cook_stages,images ))}>Добавить рецепт</button>
        </div>
    )
}





