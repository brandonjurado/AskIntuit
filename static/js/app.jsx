import React from 'react';
import ReactDOM from 'react-dom';
import './main.scss';
import ChatBot from 'react-simple-chatbot';

class App extends  React.Component {
    constructor(){
        super();
        this.initialSteps = [
              {
                id: '0',
                message: 'Hi, you can ask me your sexy tax questions!',
                trigger: '1',
              }
        ];
    }

    render() {
        return( 
            <div className="app-view">
                <ChatBot steps={this.initialSteps} />
            </div>
        );
    }
}

ReactDOM.render(<App />, document.getElementById('react-app'));
