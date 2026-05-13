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
          <p className={styles.text2}>返回首页</p>
          <p className={styles.text5}>
            <span className={styles.text3}>这</span>
            <span className={styles.text4}>
              些案例告诉我们：候鸟保护必须从静态的点位转向动态的廊道管理。只有持续追踪分布变化，识别新兴重要区域，才能在全球变化背景下守护这些空中旅人的生命征途。
              <br />
            </span>
          </p>
        </div>
        <img src="../image/mp3n72j8-2hk08xr.png" className={styles.vector} />
      </div>
    </div>
  );
}

export default Component;
