import React from "react";
class FlavorForm extends React.Component {
    constructor(props) {
        super(props);
        this.state = {value: 'coconut'};

        this.handleChange = this.handleChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
    }

    handleChange(event) {
        this.setState({value: event.target.value});
    }

    handleSubmit(event) {
        alert('Your favorite flavor is: ' + this.state.value);
        event.preventDefault();
    }

    render() {
        return (
            <form onSubmit={this.handleSubmit}>
                <label>

                    <select value={this.state.value} onChange={this.handleChange}>
                        <option value="raiting">по рейтингу↓ </option>
                        <option value="raiting">по рейтингу↑</option>
                        <option value="obr">по дате создания↓</option>
                        <option value="sozd">по дате создания↑</option>
                        <option value="randa">в случайном порядке</option>
                    </select>
                </label>
                <input type="submit" value="Submit" />
            </form>
        );
    }
}
export default FlavorForm;