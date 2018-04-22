import axios from 'axios';
import React from 'react';
import ReactDOM from 'react-dom';
import PropTypes from 'prop-types';
import { Loading } from 'react-simple-chatbot';

class Answer extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      loading: true,
      questions: undefined,
      answer: undefined,
      trigger: false,
    };
    this.triggetNext = this.triggetNext.bind(this);
  }

  componentWillMount() {
      const values = this.props.valueCallback();
       console.log(values)
       values.index = values.steps["5"].options[1].value;
       axios.get('/query/'+  values.question)
          .then((response) => {
            console.log(response);
            this.setState({ loading: false, 
              questions: response.data.questions.slice(), 
              answers: response.data.answers.slice()
            });
          })
          .catch( (error) => {
            console.log(error);
            this.setState({ loading: false, 
              questions: undefined, answers: undefined });
          });
  }

  componentWillUnMount() {
    window.answer_component_mounted = false;
  }

  triggetNext() {
    this.setState({ trigger: true }, () => {
      this.props.triggerNextStep();
    });
  }

  render() {
    console.log("rendering...")
    const { questions, answers } = this.state;

    return (
      <div className="answer-component">
        <p>{
          (questions === undefined) ? 
            < Loading />
            : ((questions.length === 0) 
            ? "Sorry nothing found." : questions[this.props.valueCallback().index])
          }
        </p>
        <p>{answers === undefined || answers.length === 0? 
          ""
          : answers[this.props.valueCallback().index] }</p>
      </div>
    );
  }
}

Answer.propTypes = {
  query: PropTypes.string,
  steps: PropTypes.object,
  triggerNextStep: PropTypes.func,
};

Answer.defaultProps = {
  query: '',
  steps: undefined,
  triggerNextStep: undefined,
};

export default Answer;