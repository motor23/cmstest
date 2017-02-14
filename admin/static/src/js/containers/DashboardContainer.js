import {bindActionCreators} from 'redux';
import {connect} from 'react-redux';
import * as actions from '../actions';
import Dashboard from '../components/dashboard';


function mapStateToProps(state) {
    return {
        dashboard: state.app.cfg.menu.dashboard
    };
}


function mapDispatchToProps(dispatch) {
    return {
        actions: bindActionCreators(actions, dispatch)
    };
}


export default connect(mapStateToProps, mapDispatchToProps)(Dashboard);