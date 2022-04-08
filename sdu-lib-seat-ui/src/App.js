import 'antd/dist/antd.css'
import './App.css';
import './components/Table'
import {Layout, Menu} from "antd";
import {
    CarryOutOutlined,
    GithubOutlined,
    HomeOutlined,
    MailOutlined,
    SettingOutlined,
    UserOutlined
} from "@ant-design/icons";
import {Link, Navigate, Route, Routes, useLocation} from "react-router-dom";
import Intro from "./components/Intro";

function App(props) {
    const location = useLocation()
    const pathSnippets = location.pathname.split('/').filter( i => i !== '');
    console.log(pathSnippets)
    const {Header, Content, Footer} = Layout;
    return (
        <div className={'sdu-lib-seat-app'} style={{height: '100%'}}>
            <Layout style={{height: '100%'}}>
                <Header style={{padding: '0'}}>
                    <Menu mode={'horizontal'} selectedKeys={[pathSnippets[0]]}>
                        <Menu.Item key={'home'} icon={<HomeOutlined />}>
                            <Link to={'/home'}>主页</Link>
                        </Menu.Item>
                        <Menu.Item key={'book'} icon={<CarryOutOutlined />}>
                            <Link to={'/book'}>预约</Link>
                        </Menu.Item>

                        <Menu.SubMenu key={'setting'} icon={<SettingOutlined />} title={'设置'}>
                            <Menu.Item key={'user'} icon={<UserOutlined />}>
                                <Link to={'/user'}>用户</Link>
                            </Menu.Item>

                            <Menu.Item key={'mail'} icon={<MailOutlined />}>
                                <Link to={'/mail'}>邮件</Link>
                            </Menu.Item>
                        </Menu.SubMenu>
                    </Menu>
                </Header>

                <Layout>
                    <Content style={{height: '100%', padding: '24px', overflow: 'auto'}}>
                        <Routes>
                            <Route path={'/home'} element={<Intro />} />
                            <Route path={'/'} element={<Navigate to={'/home'} replace />} />
                        </Routes>
                    </Content>

                    <Footer style={{ textAlign: 'center' }}>
                        SDU-LIB-SEAT ©2022 Created by <a target="_blank" href="//github.com/PTYin"><GithubOutlined /> PTYin</a>
                    </Footer>
                </Layout>
            </Layout>
        </div>
    );
}

export default App;
