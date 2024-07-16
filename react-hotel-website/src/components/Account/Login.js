import React, { useState, useContext } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Form, Button, Container, Row, Col } from 'react-bootstrap';
import APIs, { endpoints, authAPI } from "../../configs/APIs";
import cookie from "react-cookies";
import { MyDispatchContext, MyUserContext } from '../../configs/MyContext';

const Login = () => {
    const [username, setUsername] = useState(''); // Khởi tạo biến state cho username
    const [password, setPassword] = useState(''); // Khởi tạo biến state cho password
    const dispatch = useContext(MyDispatchContext);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const nav = useNavigate();

    const handleLoginError = (errorStatus) => {
        switch (errorStatus) {
            case 400:
                setError("Sai tên đăng nhập hoặc mật khẩu");
                break;
            // Xử lý các trường hợp lỗi khác nếu cần
            default:
                setError("Đăng nhập không thành công");
                break;
        }
    };



    const login = async () => {
        console.log(username); // Log username ra console để kiểm tra
        console.log(password); // Log password ra console để kiểm tra
        setError("Sai tên đăng nhập hoặc mật khẩu");
        setLoading(true);

        try {
            let res = await APIs.post(endpoints['login'], {
                'username': username,
                'password': password,
                'client_id': "4yP3PGE63tJTbxLfg19gUGgnvFeyr7oOdbEoiqk6",
                'client_secret': "dKzh5B6Q4QkebcpWczA2uJr6Ym9pzg1L4vTlzsGPuuys1TH9NVloX6qzvTClJgzJsYrGz62sryoboW1ildwapaKdEFh9OgNb95Od0iIeR0UKR1qyYam5wmdPBIEa8fF4",
                'grant_type': "password",
            }, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            });

            console.log(res.status)
            if (res.status === 200) {
                cookie.save("token", res.data.access_token);
                console.log(cookie.load("token"))
                console.log("Đăng nhập thành công!");
                console.info(res.data);
                let userdata = await authAPI(cookie.load("token")).get(endpoints['current-user']);
                cookie.save('user', userdata.data);
                dispatch({
                    "type": "login",
                    "payload": userdata.data
                });
            }
            else {
                handleLoginError(res.status); // Gọi hàm handleLoginError khi có lỗi
                console.error("Đăng nhập không thành công:", res);
            }
        } catch (ex) {
            console.error("Lỗi tại màn hình đăng nhập:", ex);
            setError("Sai tên hoặc mật khẩu, vui lòng thử lại.");
            setLoading(false);
        }
    };
    const register = () => {
        nav("/signin");
    };
    return (
        <Container className="d-flex justify-content-center align-items-center" style={{ height: '100vh' }}>
            <Row className="justify-content-md-center" >
                <Col md="6">
                    <div className="card p-4 shadow bg-white rounded">
                        <Form>
                            <h1 className="text-center mb-4">Đăng nhập</h1>
                            <Form.Group controlId="formBasicEmail">
                                <Form.Label>Tên đăng nhập</Form.Label>
                                <Form.Control
                                    type="text"
                                    placeholder="Nhập tên đăng nhập"
                                    value={username}
                                    onChange={(e) => setUsername(e.target.value)}
                                    required
                                />
                            </Form.Group>

                            <Form.Group controlId="formBasicPassword">
                                <Form.Label>Mật khẩu</Form.Label>
                                <Form.Control
                                    type="password"
                                    placeholder="Nhập mật khẩu"
                                    value={password}
                                    onChange={(e) => setPassword(e.target.value)}
                                    required
                                />
                            </Form.Group>

                            <Form.Group controlId="formBasicCheckbox" className="d-flex justify-content-between align-items-center">
                                <Form.Check type="checkbox" label="Nhớ tài khoản" />
                                <Button variant="link" onClick={() => { /* Xử lý quên mật khẩu */ }}>
                                    Quên mật khẩu
                                </Button>
                            </Form.Group>

                            <Button variant="primary" type="button" className="w-100" onClick={login}>
                                Đăng nhập
                            </Button>

                            <div className="text-center mt-3">
                                <Button variant="secondary" onClick={register}>
                                    Đăng ký
                                </Button>
                            </div>
                        </Form>
                    </div>
                </Col>
            </Row>
        </Container>
    );
}
export default Login;
