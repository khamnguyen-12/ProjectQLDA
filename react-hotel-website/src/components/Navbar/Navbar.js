/** @jsx jsx */
import { css, jsx } from '@emotion/react';
import { useState , useContext} from "react";
import Container from "../Global/Container";
import Logo from "./NavbarLogo";
import Menu from "./Menu";

import { MyUserContext } from '../../configs/MyContext';

const Navbar = () => {
    const [openMenu, setOpenMenu] = useState(false);
    const user = useContext(MyUserContext);

    return (
        <nav css={styles}>
            <Container>

                <Logo />
                <Menu openMenu={openMenu} />

                {user && user.role === 2 && (
                    <a href="/manage-bookings" className="manage-bookings">
                        Quản lý đặt phòng
                    </a>
                )}
                <i
                    onClick={() => setOpenMenu(!openMenu)}
                    id="burgerMenu"
                    className={
                        openMenu ? "fas fa-times fa-lg" : "fas fa-align-right fa-lg"
                    }
                ></i>
                
            </Container>
        </nav>
    );
};

const styles = css`
  width: 100%;
  position: fixed; /* Fix navbar vào vị trí cố định */
  top: 0; /* Hiển thị navbar ở đầu trang */
  z-index: 10;
  padding: 20px 0; /* Giảm khoảng cách giữa các thành phần */
  background-color: #0000CD;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1); /* Thêm shadow để tạo hiệu ứng nổi bật */

  .container {
    max-width: 1200px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    height: 60px; /* Chiều cao thanh navbar */
    position: relative;
  }

  .nav-actions {
    display: flex;
    align-items: center;
    gap: 20px;
  }

  .manage-bookings {
    color: #fff;
    text-decoration: none;
    text-transform: uppercase;
    font-size: 15px;
    font-weight: 600;
    position: relative;
    transition: color 700ms ease-in-out;
    &::after {
      position: absolute;
      content: "";
      background: #ff1414;
      width: 100%;
      height: 3px;
      bottom: -33px;
      left: 0;
      opacity: 0;
      transition: opacity 700ms ease-in-out;
    }
    &:hover {
      color: #ff1414;
      &::after {
        opacity: 1;
      }
    }
  }

  .user-info {
    display: flex;
    align-items: center;
    gap: 20px;
  }

  .username {
    color: #fff;
    text-decoration: none;
    font-size: 15px;
    font-weight: 600;
    text-transform: uppercase;
    position: relative;
    transition: color 700ms ease-in-out;
    &::after {
      position: absolute;
      content: "";
      background: #ff1414;
      width: 100%;
      height: 3px;
      bottom: -33px;
      left: 0;
      opacity: 0;
      transition: opacity 700ms ease-in-out;
    }
    &:hover {
      color: #ff1414;
      &::after {
        opacity: 1;
      }
    }
  }

  .logout {
    color: #fff;
    text-decoration: none;
    font-size: 15px;
    font-weight: 600;
    text-transform: uppercase;
    position: relative;
    transition: color 700ms ease-in-out;
    &::after {
      position: absolute;
      content: "";
      background: #ff1414;
      width: 100%;
      height: 3px;
      bottom: -33px;
      left: 0;
      opacity: 0;
      transition: opacity 700ms ease-in-out;
    }
    &:hover {
      color: #ff1414;
      &::after {
        opacity: 1;
      }
    }
  }

  #burgerMenu {
    cursor: pointer;
    color: #fff;
    display: none;
  }

  @media (max-width: 1200px) {
    .container {
      button {
        display: none;
      }
      #burgerMenu {
        display: block;
        position: absolute;
        top: 20px;
        right: 20px;
      }
    }
  }
`;

export default Navbar;
