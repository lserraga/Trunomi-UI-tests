from contextlib import contextmanager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import \
    staleness_of


#### from http://www.obeythetestinggoat.com/how-to-get-selenium-to-wait-for-page-load-after-a-click.html
class MySeleniumTest(SomeFunctionalTestClass):
    # assumes self.browser is a selenium webdriver

    @contextmanager
    def wait_for_page_load(self, timeout=30):
        old_page = self.browser.find_element_by_tag_name('html')
        yield
        WebDriverWait(self.browser, timeout).until(
            staleness_of(old_page)
        )

    def test_stuff(self):
        # example use
        with self.wait_for_page_load(timeout=10):
            self.browser.find_element_by_link_text('a link')
            # nice!


import {Config} from './config';
import * as jwt from 'jsonwebtoken';
import * as uuid from 'uuid';


export async function createNewUserAndLogin(enterpriseId, username, password){
    const createdAt = new Date().toISOString();
    const res1 = await Config.Db.query(
        'INSERT INTO users (created_at, username, password, enterprise_id) VALUES ($1, $2, $3, $4)',
        [createdAt, username, password, enterpriseId]
    );

    return 'Bearer ' + jwt.sign({
            sub: `${enterpriseId}::${username}`,
            pol: `enterprise on behalf of customer`,
            aud: ['Trunomi', enterpriseId, username],
            iss: enterpriseId,
            jti: uuid.v1()
        },
        Config.SigningKeys.privateKey,
        {algorithm: 'RS512'}
    );
}

export async function createNewEnterpriseSession(enterpriseId){
    const createdAt = new Date().toISOString();

    return 'Bearer ' + jwt.sign({
            sub: `${enterpriseId}`,
            pol: `enterprise`,
            aud: ['Trunomi', enterpriseId],
            iss: enterpriseId,
            jti: uuid.v1()
        },
        Config.SigningKeys.privateKey,
        {algorithm: 'RS512'}
    );
}
