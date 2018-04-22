import './main.scss';
import axios from 'axios';
import React from 'react';
import ReactDOM from 'react-dom';
import ChatBot from 'react-simple-chatbot';
import Answer from './answer.jsx';
import { ThemeProvider } from 'styled-components';


class App extends  React.Component {
    constructor(){
        super();
        
        this.state = {
            currentQuestion: '',
            currentIndex: 0,
            questions: [],
            answers: []
        };

        // all available props
        this.theme = {
            userBubbleColor: '#fff',
            userFontColor: '#4a4a4a',
        };

        this.getQueryValues = () => {
            console.log("get query value called!");
            return {
                steps: this.initialSteps,
                question: this.state.currentQuestion,
                index: this.state.currentIndex
            }
        };

        this.initialSteps = [
              { 
                id: '0',
                message: 'Hi, you can ask me your tax questions!',
                trigger: '1'
              },
              {
                id: '1',
                user: true,
                trigger: '2',
                validator: (value) => {
                    console.log("Setting state.", value);
                    this.setState({
                        currentQuestion: (value === "No") ? this.state.currentQuestion : value ,
                        currentIndex: (value === "No") ? this.state.currentIndex : 0,
                    });
                    return true;
                }
              },
              {
                id: '2',
                message: 'Here is what I found.',
                trigger: '3',
              },
              {
                id: '3',
                component: <Answer valueCallback={this.getQueryValues} />,
                trigger: '4'
              },
              {
                id: '4',
                message: 'Was this answer helpful?',
                trigger: '5'
              },
              {
                id: '5',
                options: [
                    { value: 1, label: 'Yes', trigger: '1' },
                    { value: this.getQueryValues().index++ , label: 'No', trigger: '3' },
                ]
              }
        ];

    }
    

    render() {
        return( 
            <div className="app-view">
                <div className="page">
                    <h1 className="app-header">AskIntuit!</h1>
                    <p className="pageInfo">
                        Ask Intuit questions related to tax and tax documents. 
                    </p>
                    <p className="pageInfo">
                        Get skills for alexa.
                        <br />
                        <img src="static/js/alexa_logo.svg" />
                    </p>
                    <div className="about-footer">
                        <img className="intuit-logo" src="static/js/intuit_logo.svg" />
                        <i className="devicon-amazonwebservices-plain-wordmark"></i>
                        <i className="devicon-react-original-wordmark"></i> 
                        <i className="devicon-webpack-plain-wordmark"></i>
                        <i className="devicon-babel-plain"></i>
                        <i className="devicon-python-plain-wordmark"></i>
                    </div>
                </div>
                    <ChatBot className="chatbot-ui" headerTitle="Lets talk!" steps={this.initialSteps} />
            </div>
        );
    }
}

ReactDOM.render(<App />, document.getElementById('react-app'));
