import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';

class Clock extends React.Component {
  constructor(props) {
    super(props);
    this.state = { date: new Date() };
  }

  componentDidMount() {
    this.timerID = setInterval(() => this.tick(), 1000);
  }

  componentWillUnmount() {
    clearInterval(this.timerID);
  }

  tick() {
    this.setState({
      date: new Date()
    });
  }

  render() {
    return (
      <div>
        <h1>Hello, world!</h1>
        <h2>It is {this.state.date.toLocaleTimeString()}.</h2>
      </div>
    );
  }
}

class Greeting extends React.Component {
  render() {
    return <h1>{this.props.prompt}</h1>;
  }
}

function App() {
  let prompt = 'Hello world'

  return (
    <div>
      <Greeting prompt={prompt} />
      <Clock />
      <Clock />
    </div>
  );
}
ReactDOM.render(<App />, document.getElementById('root'));
