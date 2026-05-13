import React from 'react';

import styles from './index.module.scss';

const Component = () => {
  return (
    <div className={styles.frame}>
      <p className={styles.text}>2025年雁类迁徙信息可视化</p>
      <p className={styles.visualizationOfWildG}>
        Visualization of Wild Goose Migration Information
      </p>
      <div className={styles.autoWrapper}>
        <p className={styles.wildGeeseFlySouth}>Wild geese fly south</p>
        <div className={styles.group207}>
          <div className={styles.ellipse91} />
          <div className={styles.ellipse92} />
          <div className={styles.group244}>
            <p className={styles.text4}>
              <span className={styles.text2}>雁</span>
              <span className={styles.text3}>
                类并非盲从千年不变的固定路线。它们根据气候、食物、安全等因素实时调整停歇地和越冬地。
                <br />
                <br />
              </span>
            </p>
            <img src="../image/mp3n704a-ozvwf0v.svg" className={styles.vector} />
          </div>
        </div>
      </div>
    </div>
  );
}

export default Component;
