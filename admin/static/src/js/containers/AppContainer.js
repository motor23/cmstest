import {bindActionCreators} from 'redux';
import {connect} from 'react-redux';
import * as actions from '../actions';
import App from '../components/App';


function mapStateToProps(state) {
    return {
        app: state.app
    };
}


function mapDispatchToProps(dispatch) {
    return {
        actions: bindActionCreators(actions, dispatch)
    };
}

export default connect(mapStateToProps, mapDispatchToProps)(App);