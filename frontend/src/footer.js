import React from 'react';
import { Link } from 'react-router-dom';
import { Facebook, Instagram, Twitter, Mail } from 'lucide-react';
import './App.css';

const Footer = () => {
    return (
        <footer className="footer">
            <div className="footer-container">
                <div className="footer-column">
                    <h4>O nas</h4>
                    <p className="AboutUsText">
                        BlackEagleTV to inteligentny przewodnik po filmach i serialach – rekomendujemy tytuły dopasowane do Twoich preferencji na podstawie tego, co już oglądałeś.
                    </p>
                </div>

                <div className="footer-column">
                    <h4>Linki</h4>
                    <ul>
                        <li><Link to="/">Start</Link></li>
                        <li><a href="#top">Powrót na górę</a></li>
                    </ul>
                </div>

                <div className="footer-column">
                    <h4 className="contactText"><Mail size={16} />&nbsp;Kontakt</h4>
                    <ul>
                        <li><a href="mailto:kontakt@blackeagletv.com" className="mail">kontakt@blackeagletv.com</a></li>
                    </ul>
                </div>

                <div className="footer-column">
                    <h4>Znajdź nas</h4>
                    <div className="social-icons">
                        <a href="https://facebook.com/blackeagletv" target="_blank" rel="noreferrer"><Facebook /></a>
                        <a href="https://instagram.com/blackeagletv" target="_blank" rel="noreferrer"><Instagram /></a>
                        <a href="https://twitter.com/blackeagletv" target="_blank" rel="noreferrer"><Twitter /></a>
                    </div>
                </div>
            </div>

            <div className="footer-bottom">
                © {new Date().getFullYear()} BlackEagleTV. Wszystkie prawa zastrzeżone.
            </div>
        </footer>
    );
};

export default Footer;
