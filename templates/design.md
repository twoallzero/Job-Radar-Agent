<!-- 📊 SECTION 1: 일일 요약 -->
<div style="text-align: center; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 12px; color: white; margin-bottom: 16px;">
  <h2 style="margin: 0 0 8px 0; font-size: 24px;">📊 Job Radar Daily</h2>
  <p style="margin: 0; font-size: 14px; opacity: 0.9;">채용 공고 일일 리포트</p>
  <div style="margin-top: 12px; font-size: 16px; font-weight: bold;">
    수집: <span style="color: #FFE082;">⚡{total_collected}건</span> 
    → Top <span style="color: #81C784;">✨{top10_count}건</span> 선정
  </div>
  <div style="margin-top: 8px; font-size: 13px;">⚠️ 마감 3일 이내: <span style="color: #FF5252;">{urgent_count}건</span></div>
</div>

<!-- 🏢 SECTION 2: 공고 카드 (1~10번) -->
<!-- 각 카드마다 다른 파스텔 배경색 사용 -->
<div style="background: #FFE5E5; border-radius: 12px; padding: 16px; margin-bottom: 12px; border-left: 4px solid #FF6B6B;">
  <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 12px;">
    <div>
      <h3 style="margin: 0 0 4px 0; font-size: 18px; font-weight: bold; color: #2C3E50;">[1/10] {company}</h3>
      <p style="margin: 0; font-size: 16px; color: #34495E;">{title}</p>
    </div>
    <div style="background: white; padding: 6px 12px; border-radius: 6px; font-size: 12px; font-weight: bold; color: #FF6B6B;">
      {type}
    </div>
  </div>
  
  <div style="background: rgba(255,255,255,0.6); padding: 12px; border-radius: 8px; margin-bottom: 12px; font-size: 13px; color: #555;">
    <div style="margin-bottom: 6px;">📅 <b>마감:</b> {deadline}</div>
    <div style="margin-bottom: 6px;">🔧 <b>필수:</b> {requirements}</div>
    <div>⭐ <b>추천:</b> {reason}</div>
  </div>
  
  <div style="display: flex; justify-content: space-between; align-items: center;">
    <div style="font-size: 12px; color: #888;">
      🎯 난이도: <span style="font-weight: bold; color: #E67E22;">{difficulty}</span> | 점수: {score}
    </div>
    <a href="{url}" style="background: #FF6B6B; color: white; padding: 8px 16px; border-radius: 6px; text-decoration: none; font-size: 12px; font-weight: bold;">
      공고보기 →
    </a>
  </div>
</div>

<!-- 반복되는 카드 (2~10번, 각각 다른 색상) -->
<!-- 카드 2: 옅은 복숭아색 -->
<div style="background: #FFF5E5; border-radius: 12px; padding: 16px; margin-bottom: 12px; border-left: 4px solid #FFB366;">
  <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 12px;">
    <div>
      <h3 style="margin: 0 0 4px 0; font-size: 18px; font-weight: bold; color: #2C3E50;">[2/10] {company}</h3>
      <p style="margin: 0; font-size: 16px; color: #34495E;">{title}</p>
    </div>
    <div style="background: white; padding: 6px 12px; border-radius: 6px; font-size: 12px; font-weight: bold; color: #FFB366;">
      {type}
    </div>
  </div>
  <div style="background: rgba(255,255,255,0.6); padding: 12px; border-radius: 8px; margin-bottom: 12px; font-size: 13px; color: #555;">
    <div style="margin-bottom: 6px;">📅 <b>마감:</b> {deadline}</div>
    <div style="margin-bottom: 6px;">🔧 <b>필수:</b> {requirements}</div>
    <div>⭐ <b>추천:</b> {reason}</div>
  </div>
  <div style="display: flex; justify-content: space-between; align-items: center;">
    <div style="font-size: 12px; color: #888;">
      🎯 난이도: <span style="font-weight: bold; color: #E67E22;">{difficulty}</span> | 점수: {score}
    </div>
    <a href="{url}" style="background: #FFB366; color: white; padding: 8px 16px; border-radius: 6px; text-decoration: none; font-size: 12px; font-weight: bold;">
      공고보기 →
    </a>
  </div>
</div>

<!-- 카드 3: 옅은 황색 -->
<div style="background: #FFFCE5; border-radius: 12px; padding: 16px; margin-bottom: 12px; border-left: 4px solid #FFD93D;">
  <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 12px;">
    <div>
      <h3 style="margin: 0 0 4px 0; font-size: 18px; font-weight: bold; color: #2C3E50;">[3/10] {company}</h3>
      <p style="margin: 0; font-size: 16px; color: #34495E;">{title}</p>
    </div>
    <div style="background: white; padding: 6px 12px; border-radius: 6px; font-size: 12px; font-weight: bold; color: #FFD93D;">
      {type}
    </div>
  </div>
  <div style="background: rgba(255,255,255,0.6); padding: 12px; border-radius: 8px; margin-bottom: 12px; font-size: 13px; color: #555;">
    <div style="margin-bottom: 6px;">📅 <b>마감:</b> {deadline}</div>
    <div style="margin-bottom: 6px;">🔧 <b>필수:</b> {requirements}</div>
    <div>⭐ <b>추천:</b> {reason}</div>
  </div>
  <div style="display: flex; justify-content: space-between; align-items: center;">
    <div style="font-size: 12px; color: #888;">
      🎯 난이도: <span style="font-weight: bold; color: #E67E22;">{difficulty}</span> | 점수: {score}
    </div>
    <a href="{url}" style="background: #FFD93D; color: #333; padding: 8px 16px; border-radius: 6px; text-decoration: none; font-size: 12px; font-weight: bold;">
      공고보기 →
    </a>
  </div>
</div>

<!-- 카드 4: 옅은 청색 -->
<div style="background: #E5F5FF; border-radius: 12px; padding: 16px; margin-bottom: 12px; border-left: 4px solid #4ECDC4;">
  <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 12px;">
    <div>
      <h3 style="margin: 0 0 4px 0; font-size: 18px; font-weight: bold; color: #2C3E50;">[4/10] {company}</h3>
      <p style="margin: 0; font-size: 16px; color: #34495E;">{title}</p>
    </div>
    <div style="background: white; padding: 6px 12px; border-radius: 6px; font-size: 12px; font-weight: bold; color: #4ECDC4;">
      {type}
    </div>
  </div>
  <div style="background: rgba(255,255,255,0.6); padding: 12px; border-radius: 8px; margin-bottom: 12px; font-size: 13px; color: #555;">
    <div style="margin-bottom: 6px;">📅 <b>마감:</b> {deadline}</div>
    <div style="margin-bottom: 6px;">🔧 <b>필수:</b> {requirements}</div>
    <div>⭐ <b>추천:</b> {reason}</div>
  </div>
  <div style="display: flex; justify-content: space-between; align-items: center;">
    <div style="font-size: 12px; color: #888;">
      🎯 난이도: <span style="font-weight: bold; color: #E67E22;">{difficulty}</span> | 점수: {score}
    </div>
    <a href="{url}" style="background: #4ECDC4; color: white; padding: 8px 16px; border-radius: 6px; text-decoration: none; font-size: 12px; font-weight: bold;">
      공고보기 →
    </a>
  </div>
</div>

<!-- 카드 5: 옅은 초록색 -->
<div style="background: #E5FFE5; border-radius: 12px; padding: 16px; margin-bottom: 12px; border-left: 4px solid #81C784;">
  <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 12px;">
    <div>
      <h3 style="margin: 0 0 4px 0; font-size: 18px; font-weight: bold; color: #2C3E50;">[5/10] {company}</h3>
      <p style="margin: 0; font-size: 16px; color: #34495E;">{title}</p>
    </div>
    <div style="background: white; padding: 6px 12px; border-radius: 6px; font-size: 12px; font-weight: bold; color: #81C784;">
      {type}
    </div>
  </div>
  <div style="background: rgba(255,255,255,0.6); padding: 12px; border-radius: 8px; margin-bottom: 12px; font-size: 13px; color: #555;">
    <div style="margin-bottom: 6px;">📅 <b>마감:</b> {deadline}</div>
    <div style="margin-bottom: 6px;">🔧 <b>필수:</b> {requirements}</div>
    <div>⭐ <b>추천:</b> {reason}</div>
  </div>
  <div style="display: flex; justify-content: space-between; align-items: center;">
    <div style="font-size: 12px; color: #888;">
      🎯 난이도: <span style="font-weight: bold; color: #E67E22;">{difficulty}</span> | 점수: {score}
    </div>
    <a href="{url}" style="background: #81C784; color: white; padding: 8px 16px; border-radius: 6px; text-decoration: none; font-size: 12px; font-weight: bold;">
      공고보기 →
    </a>
  </div>
</div>

<!-- 카드 6: 옅은 보라색 -->
<div style="background: #F5E5FF; border-radius: 12px; padding: 16px; margin-bottom: 12px; border-left: 4px solid #BA68C8;">
  <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 12px;">
    <div>
      <h3 style="margin: 0 0 4px 0; font-size: 18px; font-weight: bold; color: #2C3E50;">[6/10] {company}</h3>
      <p style="margin: 0; font-size: 16px; color: #34495E;">{title}</p>
    </div>
    <div style="background: white; padding: 6px 12px; border-radius: 6px; font-size: 12px; font-weight: bold; color: #BA68C8;">
      {type}
    </div>
  </div>
  <div style="background: rgba(255,255,255,0.6); padding: 12px; border-radius: 8px; margin-bottom: 12px; font-size: 13px; color: #555;">
    <div style="margin-bottom: 6px;">📅 <b>마감:</b> {deadline}</div>
    <div style="margin-bottom: 6px;">🔧 <b>필수:</b> {requirements}</div>
    <div>⭐ <b>추천:</b> {reason}</div>
  </div>
  <div style="display: flex; justify-content: space-between; align-items: center;">
    <div style="font-size: 12px; color: #888;">
      🎯 난이도: <span style="font-weight: bold; color: #E67E22;">{difficulty}</span> | 점수: {score}
    </div>
    <a href="{url}" style="background: #BA68C8; color: white; padding: 8px 16px; border-radius: 6px; text-decoration: none; font-size: 12px; font-weight: bold;">
      공고보기 →
    </a>
  </div>
</div>

<!-- 카드 7~10 (더 많은 파스텔색) -->
<!-- 카드 7: 연분홍 -->
<div style="background: #FFE5F0; border-radius: 12px; padding: 16px; margin-bottom: 12px; border-left: 4px solid #F06292;">
  <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 12px;">
    <div>
      <h3 style="margin: 0 0 4px 0; font-size: 18px; font-weight: bold; color: #2C3E50;">[7/10] {company}</h3>
      <p style="margin: 0; font-size: 16px; color: #34495E;">{title}</p>
    </div>
    <div style="background: white; padding: 6px 12px; border-radius: 6px; font-size: 12px; font-weight: bold; color: #F06292;">
      {type}
    </div>
  </div>
  <div style="background: rgba(255,255,255,0.6); padding: 12px; border-radius: 8px; margin-bottom: 12px; font-size: 13px; color: #555;">
    <div style="margin-bottom: 6px;">📅 <b>마감:</b> {deadline}</div>
    <div style="margin-bottom: 6px;">🔧 <b>필수:</b> {requirements}</div>
    <div>⭐ <b>추천:</b> {reason}</div>
  </div>
  <div style="display: flex; justify-content: space-between; align-items: center;">
    <div style="font-size: 12px; color: #888;">
      🎯 난이도: <span style="font-weight: bold; color: #E67E22;">{difficulty}</span> | 점수: {score}
    </div>
    <a href="{url}" style="background: #F06292; color: white; padding: 8px 16px; border-radius: 6px; text-decoration: none; font-size: 12px; font-weight: bold;">
      공고보기 →
    </a>
  </div>
</div>

<!-- 카드 8: 옅은 아쿠아 -->
<div style="background: #E0F7FA; border-radius: 12px; padding: 16px; margin-bottom: 12px; border-left: 4px solid #00BCD4;">
  <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 12px;">
    <div>
      <h3 style="margin: 0 0 4px 0; font-size: 18px; font-weight: bold; color: #2C3E50;">[8/10] {company}</h3>
      <p style="margin: 0; font-size: 16px; color: #34495E;">{title}</p>
    </div>
    <div style="background: white; padding: 6px 12px; border-radius: 6px; font-size: 12px; font-weight: bold; color: #00BCD4;">
      {type}
    </div>
  </div>
  <div style="background: rgba(255,255,255,0.6); padding: 12px; border-radius: 8px; margin-bottom: 12px; font-size: 13px; color: #555;">
    <div style="margin-bottom: 6px;">📅 <b>마감:</b> {deadline}</div>
    <div style="margin-bottom: 6px;">🔧 <b>필수:</b> {requirements}</div>
    <div>⭐ <b>추천:</b> {reason}</div>
  </div>
  <div style="display: flex; justify-content: space-between; align-items: center;">
    <div style="font-size: 12px; color: #888;">
      🎯 난이도: <span style="font-weight: bold; color: #E67E22;">{difficulty}</span> | 점수: {score}
    </div>
    <a href="{url}" style="background: #00BCD4; color: white; padding: 8px 16px; border-radius: 6px; text-decoration: none; font-size: 12px; font-weight: bold;">
      공고보기 →
    </a>
  </div>
</div>

<!-- 카드 9: 옅은 라임 -->
<div style="background: #F1F8E9; border-radius: 12px; padding: 16px; margin-bottom: 12px; border-left: 4px solid #CDDC39;">
  <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 12px;">
    <div>
      <h3 style="margin: 0 0 4px 0; font-size: 18px; font-weight: bold; color: #2C3E50;">[9/10] {company}</h3>
      <p style="margin: 0; font-size: 16px; color: #34495E;">{title}</p>
    </div>
    <div style="background: white; padding: 6px 12px; border-radius: 6px; font-size: 12px; font-weight: bold; color: #CDDC39;">
      {type}
    </div>
  </div>
  <div style="background: rgba(255,255,255,0.6); padding: 12px; border-radius: 8px; margin-bottom: 12px; font-size: 13px; color: #555;">
    <div style="margin-bottom: 6px;">📅 <b>마감:</b> {deadline}</div>
    <div style="margin-bottom: 6px;">🔧 <b>필수:</b> {requirements}</div>
    <div>⭐ <b>추천:</b> {reason}</div>
  </div>
  <div style="display: flex; justify-content: space-between; align-items: center;">
    <div style="font-size: 12px; color: #888;">
      🎯 난이도: <span style="font-weight: bold; color: #E67E22;">{difficulty}</span> | 점수: {score}
    </div>
    <a href="{url}" style="background: #CDDC39; color: #333; padding: 8px 16px; border-radius: 6px; text-decoration: none; font-size: 12px; font-weight: bold;">
      공고보기 →
    </a>
  </div>
</div>

<!-- 카드 10: 옅은 주황 -->
<div style="background: #FFE8D6; border-radius: 12px; padding: 16px; margin-bottom: 12px; border-left: 4px solid #FF9800;">
  <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 12px;">
    <div>
      <h3 style="margin: 0 0 4px 0; font-size: 18px; font-weight: bold; color: #2C3E50;">[10/10] {company}</h3>
      <p style="margin: 0; font-size: 16px; color: #34495E;">{title}</p>
    </div>
    <div style="background: white; padding: 6px 12px; border-radius: 6px; font-size: 12px; font-weight: bold; color: #FF9800;">
      {type}
    </div>
  </div>
  <div style="background: rgba(255,255,255,0.6); padding: 12px; border-radius: 8px; margin-bottom: 12px; font-size: 13px; color: #555;">
    <div style="margin-bottom: 6px;">📅 <b>마감:</b> {deadline}</div>
    <div style="margin-bottom: 6px;">🔧 <b>필수:</b> {requirements}</div>
    <div>⭐ <b>추천:</b> {reason}</div>
  </div>
  <div style="display: flex; justify-content: space-between; align-items: center;">
    <div style="font-size: 12px; color: #888;">
      🎯 난이도: <span style="font-weight: bold; color: #E67E22;">{difficulty}</span> | 점수: {score}
    </div>
    <a href="{url}" style="background: #FF9800; color: white; padding: 8px 16px; border-radius: 6px; text-decoration: none; font-size: 12px; font-weight: bold;">
      공고보기 →
    </a>
  </div>
</div>

<!-- 🚨 SECTION 3: 긴급 마감 알림 (3일 이내) -->
<div style="background: linear-gradient(135deg, #FF6B6B 0%, #FF5252 100%); border-radius: 12px; padding: 16px; margin-bottom: 16px; color: white;">
  <h3 style="margin: 0 0 12px 0; font-size: 18px;">🚨 마감 3일 이내 긴급 공고</h3>
  <div style="font-size: 13px; line-height: 1.8;">
    • <b>{company1}</b> — {title1}<br>
    &nbsp;&nbsp;마감: {deadline1} | <a href="{url1}" style="color: #FFE082; text-decoration: none;">보러가기</a><br><br>
    • <b>{company2}</b> — {title2}<br>
    &nbsp;&nbsp;마감: {deadline2} | <a href="{url2}" style="color: #FFE082; text-decoration: none;">보러가기</a>
  </div>
</div>

<!-- ✍️ SECTION 4: 커버레터 초안 완료 -->
<div style="background: linear-gradient(135deg, #4ECDC4 0%, #44A08D 100%); border-radius: 12px; padding: 16px; margin-bottom: 16px; color: white;">
  <h3 style="margin: 0 0 8px 0; font-size: 18px;">✍️ 지원 동기 초안 작성 완료</h3>
  <p style="margin: 8px 0; font-size: 13px; opacity: 0.95;">
    다음 공고들의 커버레터 초안이 생성되었습니다. <code style="background: rgba(0,0,0,0.2); padding: 2px 6px; border-radius: 3px;">./drafts/</code>에서 확인하세요.
  </p>
  <div style="background: rgba(0,0,0,0.15); padding: 10px; border-radius: 6px; margin-top: 10px; font-size: 12px; font-family: monospace;">
    📄 cover_20260514_01_{company1}.md<br>
    📄 cover_20260514_02_{company2}.md<br>
    📄 cover_20260514_03_{company3}.md
  </div>
</div>

<!-- 📌 SECTION 5: 푸터 -->
<div style="text-align: center; padding: 16px; background: #F8F9FA; border-radius: 12px; border-top: 2px solid #DDD; font-size: 12px; color: #666;">
  <p style="margin: 0 0 8px 0;">
    🤖 <b>Job Radar Agent</b> v2.0
  </p>
  <p style="margin: 0 0 8px 0;">
    명령어: <code style="background: white; padding: 2px 6px; border-radius: 3px;">/도움</code> 
    | <code style="background: white; padding: 2px 6px; border-radius: 3px;">/실행</code> 
    | <code style="background: white; padding: 2px 6px; border-radius: 3px;">/현황</code>
  </p>
  <p style="margin: 0;">
    📅 {date} | ⏱️ {elapsed}초 소요
  </p>
</div>
